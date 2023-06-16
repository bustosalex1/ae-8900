export const deepCopy = (item: object) => {
    return JSON.parse(JSON.stringify(item))
}
