document.addEventListener('DOMContentLoaded', (event) => {
    const checkboxes = document.querySelectorAll('#directory-list input[type="checkbox"]');
    const uncheckedList = document.getElementById('unchecked-list');
    const numImagesInput = document.getElementById('num-images-input');
    const thresholdInput = document.getElementById('threshold-input');
    const widthInput = document.getElementById('width-input');
    const heightInput = document.getElementById('height-input');
    const numImagesBtn = document.getElementById('num-images-btn');
    const numImagesClassInput = document.getElementById('num-images-class-input');
    const numImagesClassBtn = document.getElementById('num-images-class-btn');
    const TrainBtn = document.getElementById('train-btn');
    const classifyImgsBtn = document.getElementById('classify-imgs-btn');
    const resultsDiv = document.getElementById('results');
    const imageDisplayDiv = document.getElementById('image-display');

    let numImages = 0;
    let numImagesClass = 0;
    thresholdInput.value = 0.01;
    widthInput.value = 100;
    heightInput.value = 100;

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
            thresholdInput.disabled = true;
            widthInput.disabled = true;
            heightInput.disabled = true;
            numImagesClassBtn.disabled = false;
            numImagesClassInput.disabled = false;
            numImagesBtn.disabled = true;
            numImagesInput.disabled = true;
        } else {
            alert("Please enter a valid number of images.");
        }
    });

    numImagesClassBtn.addEventListener('click', () => {
        numImagesClass = parseInt(numImagesClassInput.value);
        if (!isNaN(numImagesClass) && numImagesClass > 0) {
            TrainBtn.disabled = false;
            numImagesClassBtn.disabled = true;
            numImagesClassInput.disabled = true;
        } else {
            alert("Please enter a valid number of images.");
        }
    });

    TrainBtn.addEventListener('click', () => {
        const uncheckedFolders = [];
        checkboxes.forEach(checkbox => {
            if (!checkbox.checked) {
                uncheckedFolders.push(checkbox.name);
            }
        });
        
        resultsDiv.innerHTML = `Training classes...`;
        fetch('/train', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                folders: uncheckedFolders, 
                num_images: numImages, 
                threshold: parseFloat(thresholdInput.value), 
                width: parseInt(widthInput.value), 
                height: parseInt(heightInput.value) 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Variable set successfully:", data);
                classifyImgsBtn.disabled = false;
                TrainBtn.disabled = true;
                displayImages(data.image_paths);
                resultsDiv.innerHTML = `Images used for training:`;
            } else {
                console.error("Failed to set variable");
            }
        })
        .catch(error => {
            console.error("Error setting variable:", error);
        });
    });

    classifyImgsBtn.addEventListener('click', () => {
        resultsDiv.innerHTML = `Classifying images...`;
        fetch('/classify_imgs', {
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
        thresholdInput.disabled = false;
        widthInput.disabled = false;
        heightInput.disabled = false;
        numImagesBtn.disabled = false;
        numImagesInput.disabled = false;
        classifyImgsBtn.disabled = true;
    });

    function displayImages(imagePaths) {
        imageDisplayDiv.innerHTML = '';
        const divDict = {};
        imagePaths.forEach(path => {
            const imgSrc = path[0];
            const divKey = path[1];

            if (!divDict[divKey]) {
                const newDiv = document.createElement('div');
                newDiv.id = divKey;
                newDiv.style.margin = '20px';

                const toggleButton = document.createElement('button');
                toggleButton.textContent = divKey;
                toggleButton.addEventListener('click', () => {
                    const images = newDiv.querySelectorAll('img');
                    images.forEach(img => {
                        img.style.display = img.style.display === 'none' ? 'block' : 'none';
                    });
                });

                newDiv.appendChild(toggleButton);
                imageDisplayDiv.appendChild(newDiv);
                divDict[divKey] = newDiv;
            }

            const img = document.createElement('img');
            img.src = imgSrc;
            img.alt = 'Selected Image';
            img.style.width = '100px';
            img.style.height = '100px';
            img.style.display = 'none'; // Add this line to display images vertically
            divDict[divKey].appendChild(img);
        });
    }

    // Initial population of the unchecked list
    updateUncheckedList();
});