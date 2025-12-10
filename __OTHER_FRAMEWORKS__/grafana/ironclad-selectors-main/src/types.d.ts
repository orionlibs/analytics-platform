export type AttributesMap<T extends string = string> = Record<
  T,
  string | null
> | null

export interface Model {
  text: string | null
  tag: string
  isNotable: boolean
  attributes: AttributesMap
}

export type Preferences = `attributes` | `text`

export interface Options {
  inclusions: {
    // The order of these matter - it favours using the first over the latter
    attributes: string[]
    notableTags: string[]
  }
  preferences: Preferences[]
}
