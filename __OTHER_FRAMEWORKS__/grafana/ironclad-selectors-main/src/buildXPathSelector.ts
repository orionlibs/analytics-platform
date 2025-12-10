export function buildXPathSelector(selectorChain: Array<string | null>) {
  return selectorChain.reduce<string>((acc, curr) => {
    if (curr) {
      return `${acc}${curr}`
    }

    return acc
  }, ``)
}
