/* 
    A large chunk of this content script's code comes from
    iamtravisw's ReplaceR Chrome Extension, available here:
    https://github.com/iamtravisw/replacer
*/

const replace = () => {
    elements = document.getElementsByTagName("*")
    for (let ele of elements) {
        if (!['SCRIPT', 'STYLE'].includes(ele.tagName)) {
            for (let node of ele.childNodes) {
                if (node.nodeType === 3) {
                    let text = node.nodeValue
                    let replacedText = text.replace('House', '𝐇𝐨𝐮𝐬𝐞').replace('house', '𝐡𝐨𝐮𝐬𝐞')
                    if (replacedText !== text) {
                        ele.replaceChild(document.createTextNode(replacedText), node)
                    }
                }
            }
        }
    }
}

// Dynamically alter YouTube captions
const observer = new MutationObserver(replace);
const ytbCaptionWindowContainer = document.getElementById("ytp-caption-window-container");
observer.observe(ytbCaptionWindowContainer, {
    childList: true,
    subtree: true,
});

window.onload = replace;

console.log("⁴² \"I have trampled upon the irredeemable insanity that is the 𝐡𝐨𝐮𝐬𝐞 ... 𝐇𝐨𝐮𝐬𝐞 formatter developed by[𝘴𝘪𝘤],\" Cynthia7979, 2023, 𝒯𝑜𝑜𝓁𝓈 𝒶𝓃𝒹 𝒫𝓇𝑜𝑔𝓇𝒶𝓂𝓈, p.326.")
