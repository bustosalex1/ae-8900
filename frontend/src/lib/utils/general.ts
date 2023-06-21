/**
 * Create a deep copy of something that is JSON serializable.
 */
export const deepCopy = (item: object) => {
    return JSON.parse(JSON.stringify(item))
}

/**
 * A filthy hack.
 */
export const noTypeCheck = (x: any) => x
