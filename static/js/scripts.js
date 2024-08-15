document.addEventListener('DOMContentLoaded', (event) => {
    const checkboxes = document.querySelectorAll('#directory-list input[type="checkbox"]');
    const uncheckedList = document.getElementById('unchecked-list');
    const numImagesInput = document.getElementById('num-images-input');
    const numImagesBtn = document.getElementById('num-images-btn');
    const numImagesClassInput = document.getElementById('num-images-class-input');
    const numImagesClassBtn = document.getElementById('num-images-class-btn');
    const setVariableBtn = document.getElementById('set-variable-btn');
    const classifyDirsBtn = document.getElementById('classify-dirs-btn');
    const resultsDiv = document.getElementById('results');
    const imageDisplayDiv = document.getElementById('image-display');

    let numImages = 0;
    let numImagesClass = 0;

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            updateUncheckedList();
        });
    });

    function updateUncheckedList() {
        uncheckedList.innerHTML = '';
        checkboxes.forEach(checkbox => {
            if (!checkbox.checked) {
                const li = document.createElement('li');
                li.textContent = checkbox.name;
                uncheckedList.appendChild(li);
            }
        });
    }

    numImagesBtn.addEventListener('click', () => {
        numImages = parseInt(numImagesInput.value);
        if (!isNaN(numImages) && numImages > 0) {
            numImagesClassBtn.disabled = false;
            numImagesBtn.disabled = true;
        } else {
            alert("Please enter a valid number of images.");
        }
    });

    numImagesClassBtn.addEventListener('click', () => {
        numImagesClass = parseInt(numImagesClassInput.value);
        if (!isNaN(numImagesClass) && numImagesClass > 0) {
            setVariableBtn.disabled = false;
            numImagesClassBtn.disabled = true;
        } else {
            alert("Please enter a valid number of images.");
        }
    });

    setVariableBtn.addEventListener('click', () => {
        const uncheckedFolders = [];
        checkboxes.forEach(checkbox => {
            if (!checkbox.checked) {
                uncheckedFolders.push(checkbox.name);
            }
        });

        console.log("Setting variable with folders:", uncheckedFolders, "and number of images:", numImages);

        fetch('/set_variable', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ folders: uncheckedFolders, num_images: numImages })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Variable set successfully:", data);
                classifyDirsBtn.disabled = false;
                setVariableBtn.disabled = true;
                displayImages(data.image_paths);
            } else {
                console.error("Failed to set variable");
            }
        })
        .catch(error => {
            console.error("Error setting variable:", error);
        });
    });

    classifyDirsBtn.addEventListener('click', () => {
        console.log("classify_dirs button clicked");
        resultsDiv.innerHTML = `Classifying directories...`;
        fetch('/classify_dirs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ num_images: numImagesClass })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Classification successful:", data);
                resultsDiv.innerHTML = `
                    <p>${data.perCorrect}% of images were correctly classified with ${data.confidence}% confidence.</p>
                    <p>${data.perIncorrect}% of images were incorrectly classified.</p>
                `;
            } else {
                console.error("Classification failed:", data.message);
            }
        })
        .catch(error => {
            console.error("Error classifying directories:", error);
        });
        numImagesBtn.disabled = false;
        classifyDirsBtn.disabled = true;
    });

    function displayImages(imagePaths) {
        imageDisplayDiv.innerHTML = '';
        imagePaths.forEach(path => {
            const img = document.createElement('img');
            img.src = path;
            img.alt = 'Selected Image';
            img.style.width = '100px';
            img.style.height = '100px';
            img.style.display = 'block'; // Add this line to display images vertically
            imageDisplayDiv.appendChild(img);
        });
    }

    // Initial population of the unchecked list
    updateUncheckedList();
});