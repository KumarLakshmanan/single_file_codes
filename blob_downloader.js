// List of "blob:https://web.whatsapp.com/b39ee520-ca5e-4537-b200-f6f98658f5b0"
var blobImages = []
document.querySelectorAll('img.x10e4vud').forEach((img) => {
    blobImages.push(img.src)
});
console.log(blobImages);
var i = 0;
setInterval(() => {
    if (i < blobImages.length) {
        fetch(blobImages[i])
            .then(res => res.blob())
            .then(blob => {
                var fileName = blobImages[i].split("/").pop();
                const file = new File([blob], `${fileName}.png`, { type: 'image/png' });
                const a = document.createElement('a');
                a.href = URL.createObjectURL(file);
                a.download = `${fileName}.png`;
                a.click();
                i++;
            });
    }    
}, 100);
