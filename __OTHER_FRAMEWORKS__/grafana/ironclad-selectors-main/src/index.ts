import { getXPathSelectorChain } from "getXPathSelectorChain"
import { buildXPathSelector } from "buildXPathSelector"
import { getModel } from "getModel"
import { Options, Model } from "./types"
import { checkCriteria } from "checkCriteria"
import { FAIL_CRITERIA } from "consts"

const DEFAULT_OPTIONS: Options = {
  inclusions: {
    attributes: [`data-testid`, `id`, `href`],
    notableTags: [`a`, `button`, `form`, `input`],
  },
  preferences: [`text`, `attributes`],
}

interface Props {
  element: HTMLElement
  options: Options
  chain?: Model[]
  preferenceIndex?: number
}

let originalElement: HTMLElement | null = null

function select({ element, options, chain = [], preferenceIndex = 0 }: Props) {
  if (chain.length === 0) {
    originalElement = element
  }

  const preference = options.preferences[preferenceIndex] || null
  const model = getModel(element, options, preference)
  const selectorChain = getXPathSelectorChain([model, ...chain], options)
  const xPathSelector = buildXPathSelector(selectorChain)
  const failCriteria = checkCriteria(xPathSelector, options)

  console.log({
    chain,
    preference,
    model,
    selectorChain,
    xPathSelector,
    failCriteria,
  })

  // found good selector
  if (!failCriteria) {
    return xPathSelector
  }

  // it was probably removed from the DOM. Is this a safe assumption?
  if (failCriteria.type === FAIL_CRITERIA.NO_ELEMENTS_FOUND) {
    return xPathSelector
  }

  // try with new preference
  const newIndex = preferenceIndex + 1
  const wouldHaveNewPreference = Boolean(options.preferences[newIndex])

  if (failCriteria && wouldHaveNewPreference) {
    return select({
      element,
      options,
      chain,
      preferenceIndex: newIndex,
    })
  }

  const parentElement = element.parentElement

  if (!parentElement) {
    // todo: retry and resort to DOM strcture
    console.log({
      originalElement,
      selectorChain,
      xPathSelector,
      failCriteria,
    })

    throw new Error(`No good selector found`)
  }

  return select({
    element: parentElement,
    options,
    chain: [model, ...chain],
  })
}

document.addEventListener(`click`, (e) => {
  console.log(e.target)
  const element = e.target as HTMLElement
  const selectorChain = select({ element, options: DEFAULT_OPTIONS })

  console.log(selectorChain)
})
