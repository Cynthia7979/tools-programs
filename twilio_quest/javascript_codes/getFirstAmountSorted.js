function getFirstAmountSorted(firstArgument, secondArgument) {
    let sortedArray = firstArgument.sort();
    return sortedArray.slice(0, secondArgument);
}