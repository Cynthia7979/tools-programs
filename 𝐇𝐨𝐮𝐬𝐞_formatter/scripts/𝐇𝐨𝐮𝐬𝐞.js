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

window.onload = () => {
    // Initial pass to replace 𝐡𝐨𝐮𝐬𝐞s
    replace()
    
    // Dynamically alter dynamic elements
    if (window.location) {
        const url = window.location.origin;
        if (url && url.includes("youtube.com")) {
            // Captions
            const ytElementIds = ["ytp-caption-window-container", "chat-container"]
            for (let contentId of ytElementIds) {
                let ytElement = document.getElementById(contentId);
                console.log(contentId)
                console.log(ytElement)
                if (ytElement) {
                    let observer = new MutationObserver(() => {console.log(`change! ${contentId}`); replace()});
                    observer.observe(
                        ytElement, {
                        childList: true,
                        subtree: true,
                    });
                }
            }
    
            // YouTube live chat (not working)
            // const chatiframe = document.getElementById("chatframe")
            // if (chatiframe) {
            //     const originaliFrameOnload = chatiframe.onload
    
            //     // YouTube live chat update once
            //     chatiframe.onload = (e) => {
            //         originaliFrameOnload(e)
            //         const iFrame = document.getElementById("chatframe")
            //         console.log(iFrame.contentWindow.document)
            //     }
            // }
        }
    }
}

console.log("⁴² \"I have trampled upon the irredeemable insanity that is the 𝐡𝐨𝐮𝐬𝐞 ... 𝐇𝐨𝐮𝐬𝐞 formatter developed by[𝘴𝘪𝘤],\" Cynthia7979, 2023, 𝒯𝑜𝑜𝓁𝓈 𝒶𝓃𝒹 𝒫𝓇𝑜𝑔𝓇𝒶𝓂𝓈, p.326.")
