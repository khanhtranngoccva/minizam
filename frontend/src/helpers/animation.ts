export async function waitForAnimationFrame() {
    return new Promise(resolve => {
        requestAnimationFrame((timestamp) => {
            resolve(timestamp);
        });
    });
}