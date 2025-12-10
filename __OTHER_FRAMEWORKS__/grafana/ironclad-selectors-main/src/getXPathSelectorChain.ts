import { Model, Options } from "./types"

export function getXPathSelectorChain(
  modelChain: Model[],
  options: Options
): Array<string | null> {
  return modelChain.map((model, i) => {
    const isEndOfChain = i === modelChain.length - 1
    const notableTag = model.isNotable && model.tag
    const tag = notableTag || `*`
    const attribute = getAttributeToUse(model, options)
    const text = getText(model, options)
    const ignore = !notableTag && !attribute && !text

    if (ignore) {
      // this is the original element so we have to establish it as the target
      if (isEndOfChain) {
        return `//${model.tag}`
      }

      return null
    }

    return `//${tag}${attribute}${text}`
  })
}

function getAttributeToUse(model: Model, options: Options) {
  const attributes = model.attributes
  const notableAttributes = options.inclusions.attributes

  for (const attribute of notableAttributes) {
    const value = attributes?.[attribute]

    if (value) {
      return `[@${attribute}="${value}"]`
    }
  }

  return ``
}

function getText(model: Model, options: Options) {
  const includeText = options.preferences.includes(`text`)

  if (!includeText || !model.text) {
    return ``
  }

  return `[text()="${model.text}"]`
}
