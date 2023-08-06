use super::object;
use super::Group;

use anyhow::Context;
use anyhow::Result;
use quick_xml::events::BytesStart;
use quick_xml::events::Event;

use std::io::BufRead;

pub(crate) fn leading_events<R: BufRead>(
    reader: &mut quick_xml::Reader<R>,
    buffer: &mut Vec<u8>,
) -> Result<(Vec<Event<'static>>, Option<BytesStart<'static>>)> {
    let mut out = Vec::new();

    while let Ok(event) = reader.read_event(buffer) {
        let event = event.into_owned();

        if let Event::Start(element) = event {
            if element.name() == b"g" {
                return Ok((out, Some(element)));
            } else {
                out.push(Event::Start(element));
            }
        } else {
            out.push(event);
        }
    }

    Ok((out, None))
}

pub(crate) fn trailing_events<R: BufRead>(
    reader: &mut quick_xml::Reader<R>,
    buffer: &mut Vec<u8>,
    first_trailing_event: Event<'static>,
) -> Result<Vec<Event<'static>>> {
    let mut out = Vec::new();

    out.push(first_trailing_event);
    while let Ok(event) = reader.read_event(buffer) {
        if let Event::Eof = event {
            break;
        } else {
            out.push(event.into_owned())
        }
    }

    Ok(out)
}

pub(in crate::inkscape) fn layers<R: BufRead>(
    reader: &mut quick_xml::Reader<R>,
    buffer: &mut Vec<u8>,
    first_layer_start: BytesStart<'static>,
) -> Result<(Vec<Group>, Event<'static>)> {
    let mut out = Vec::new();

    let first_group = group(first_layer_start, reader, buffer)?;
    out.push(first_group);

    while let Ok(event) = reader.read_event(buffer) {
        let event = event.into_owned();

        if let Event::Start(ref element) = event {
            if element.name() == b"g" {
                // we are at the first layer event, leave this function

                //return Ok((out, Some(event)))
            }
        } else {
            return Ok((out, event));
        }
    }

    unreachable!()

    //Ok((out, None))
}

/// parse all the contents (including header tag) of `<g> ... </g>` elements
pub(in crate::inkscape) fn group<R: BufRead>(
    start_event: BytesStart<'static>,
    reader: &mut quick_xml::Reader<R>,
    buffer: &mut Vec<u8>,
) -> Result<Group> {
    let mut content = Vec::new();

    let mut footer = None;

    while let Ok(event) = reader.read_event(buffer) {
        let event = event.into_owned();

        match event {
            Event::Empty(xml_object) => {
                // parse the object
                let object = object(xml_object).with_context(|| {
                    let name = layer_name(&start_event).unwrap();
                    format!("failed to parse object in layer {name}")
                })?;

                content.push(object);
            }
            Event::End(end) => {
                footer = Some(Event::End(end));
                break;
            }
            other_event => {
                content.push(object::Object::Other(other_event));
            }
        }
    }

    let footer = if let Some(inner_footer) = footer {
        inner_footer
    } else {
        let name = layer_name(&start_event)?;
        anyhow::bail!("failed to find end of group attribute for layer {}", name)
    };

    let grp = Group {
        header: Event::Start(start_event),
        content,
        footer,
    };

    Ok(grp)
}

/// map an element inside <g>... </g> to a `Object` that may be adjusted
/// by the user
pub(crate) fn object(element: BytesStart<'static>) -> Result<object::Object> {
    let obj = match element.name() {
        b"image" => {
            // parse as an image
            let ident = object::Identifiers::from_elem(&element).with_context(|| {
                format!(
                    "failed to parse image id / width / height from element {:?}",
                    element
                )
            })?;

            object::Object::Image(object::Image { ident, element })
        }
        b"rect" => {
            // parse as a rectangle
            let ident = object::Identifiers::from_elem(&element).with_context(|| {
                format!(
                    "failed to parse rectangle id / width / height from element {:?}",
                    element
                )
            })?;

            object::Object::Rectangle(object::Rectangle { ident, element })
        }
        _unknown => object::Object::Other(Event::Empty(element)),
    };

    Ok(obj)
}

fn layer_name(layer_start_event: &BytesStart<'static>) -> Result<String> {
    let (_, name_id) = layer_start_event
        .attributes()
        .into_iter()
        .filter_map(|x| x.ok())
        .map(|att| (att.key, att.value))
        .find(|(key, _)| key == &b"id".as_slice())
        .unwrap();

    Ok(String::from_utf8(name_id.to_vec())?)
}

fn utf8_name(event: BytesStart<'_>) -> Result<String> {
    String::from_utf8(event.name().to_vec()).with_context(|| {
        format!(
            "failed to convert bytes sequence to UTF8 name: {:?}",
            event.name()
        )
    })
}
