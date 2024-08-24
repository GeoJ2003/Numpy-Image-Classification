document.addEventListener('DOMContentLoaded', (event) => {
    const directoryList = document.getElementById('directory-list');
    const numImagesInput = document.getElementById('num-images-input');
    const thresholdSlider = document.getElementById('threshold-slider');
    const thresholdValue = document.getElementById('threshold-value');
    const widthInput = document.getElementById('width-input');
    const heightInput = document.getElementById('height-input');
    const settingsBtn = document.getElementById('settings-btn');
    const numImagesBtn = document.getElementById('num-images-btn');
    const numImagesClassInput = document.getElementById('num-images-class-input');
    const numImagesClassBtn = document.getElementById('num-images-class-btn');
    const TrainBtn = document.getElementById('train-btn');
    const classifyImgsBtn = document.getElementById('classify-imgs-btn');
    const resultsDiv = document.getElementById('results');
    const imageDisplayDiv = document.getElementById('image-display');
    let dir_dict = {};
    let subdirs_selected = {};

    function listDirectories() {
        fetch('/get_directories', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            dir_dict = data['dir_dict'];
            console.log(Object.keys(dir_dict));
            console.log(Object.values(dir_dict));

            // Clear existing list
            directoryList.innerHTML = '';

            // Iterate for each key in the dictionary
            Object.keys(dir_dict).forEach((key) => {
                const header = document.createElement('h3');
                const toggleButton = document.createElement('button');
                toggleButton.textContent = key;
                toggleButton.style.background = 'none';
                toggleButton.style.border = 'none';
                toggleButton.style.color = 'inherit';
                toggleButton.style.font = 'inherit';
                toggleButton.style.cursor = 'pointer';
                toggleButton.title = 'Click to expand directory';

                toggleButton.addEventListener('click', () => {
                    const subdirectories = header.querySelectorAll('li');
                    subdirectories.forEach(subdir => {
                        subdir.style.display = subdir.style.display === 'none' ? 'block' : 'none';
                    });
                });

                directoryList.appendChild(header);
                header.appendChild(toggleButton);

                Object.values(dir_dict[key]).forEach((value) => {
                    const li = document.createElement('li');
                    li.style.display = 'none';

                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.name = value;
                    checkbox.id = value;

                    // Add event listener to the checkbox
                    checkbox.addEventListener('change', (event) => {
                        handleCheckboxChange(event);
                    });

                    const link = document.createElement('a');
                    link.href = `imgs/${key}/${value}`;
                    link.textContent = value;

                    li.appendChild(checkbox);
                    li.appendChild(link);
                    header.appendChild(li);
                });
            });
        });
    }

    function handleCheckboxChange(event) {
        const checkbox = event.target;
        const value = checkbox.id;
        const keys = Object.keys(dir_dict);
        keys.forEach((key) => {
            if (dir_dict[key].includes(value)) {
                if (Object.keys(subdirs_selected).length !== 0 && !Object.values(subdirs_selected).includes(key)) {
                    resultsDiv.innerHTML = 'Please select sub directories from the same directory.';
                    return;
                }
                if (checkbox.checked) {
                    subdirs_selected[value] = key;
                    console.log(subdirs_selected);
                } else {
                    delete subdirs_selected[value];
                }
            }
        });
    }

    listDirectories();

    thresholdSlider.addEventListener('input', () => {
        thresholdValue.textContent = thresholdSlider.value;
    });

    let leastNumImages = 2;

    settingsBtn.addEventListener('click', () => {
        imageDisplayDiv.innerHTML = '';
        resultsDiv.innerHTML = '';

        if (Object.keys(subdirs_selected).length < 2) {
            resultsDiv.innerHTML = 'Please select 2 or more sub directories to train.';
            return;
        }

        if (isNaN(parseInt(widthInput.value)) || isNaN(parseInt(heightInput.value))) {
            resultsDiv.innerHTML = `Please enter valid values for the width, and height.`;
        } else {
            fetch('/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    dirs: subdirs_selected
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    leastNumImages = data.min_images;
                } else {
                    console.error("Failed to set directories:", data.message);
                }
            })
            const threshold = parseFloat(thresholdSlider.value);
            const width = parseInt(widthInput.value);
            const height = parseInt(heightInput.value);
            thresholdSlider.disabled = true;
            widthInput.disabled = true;
            heightInput.disabled = true;
            settingsBtn.disabled = true;
            numImagesBtn.disabled = false;
            numImagesInput.disabled = false;
            resultsDiv.innerHTML = 'Select a number of images for training.';
        }
    });

    numImagesBtn.addEventListener('click', () => {
        if (isNaN(parseInt(numImagesInput.value))) {
            resultsDiv.innerHTML = `Please enter a valid value for the number of images to train.`;
        }
        else if (parseInt(numImagesInput.value) < 2) {
            resultsDiv.innerHTML = `Please select a number of images greater than 1.`;
        }
        else if (parseInt(numImagesInput.value) > leastNumImages - 1) {
            resultsDiv.innerHTML = `Please select a number of images less than or equal to ${leastNumImages - 1}.`;
        }
        else {
            leastNumImages = leastNumImages - parseInt(numImagesInput.value);
            numImagesBtn.disabled = true;
            numImagesInput.disabled = true;
            numImagesClassBtn.disabled = false;
            numImagesClassInput.disabled = false;
            resultsDiv.innerHTML = 'Select a number of images to classify.';
        }
    });

    numImagesClassBtn.addEventListener('click', () => {
        const numImagesClass = parseInt(numImagesClassInput.value);
        if (isNaN(numImagesClass)) {
            resultsDiv.innerHTML = `Please enter a valid value for the number of images to classify.`;
        } else if (numImagesClass < 2) {
            resultsDiv.innerHTML = `Please select a number of images greater than 1.`;
        } else if (numImagesClass > leastNumImages) {
            resultsDiv.innerHTML = `Please select a number of images less than or equal to ${leastNumImages}.`;
        }
        else {
            numImagesClassBtn.disabled = true;
            numImagesClassInput.disabled = true;
            TrainBtn.disabled = false;
            resultsDiv.innerHTML = 'Click the train button to create subclasses for each directory chosen.';
        }
    });

    TrainBtn.addEventListener('click', () => {
        const uncheckedFolders = [];
        TrainBtn.disabled = true;
        key = Object.values(subdirs_selected)[0];
        console.log(key);

        dir_dict[key].forEach((value) => {
            if (!Object.keys(subdirs_selected).includes(value)) {
                uncheckedFolders.push(value);
            }
        });
        console.log(uncheckedFolders);
        
        resultsDiv.innerHTML = `Training classes...`;
        fetch('/train', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                dir: key,
                folders: uncheckedFolders, 
                num_images: parseInt(numImagesInput.value), 
                threshold: parseFloat(thresholdSlider.value), 
                width: parseInt(widthInput.value), 
                height: parseInt(heightInput.value) 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                classifyImgsBtn.disabled = false;
                displayImages(data.image_paths);
                resultsDiv.innerHTML = `Images used for training:`;
            } else {
                console.error("Failed to create matrix classes");
            }
        })
        .catch(error => {
            console.error("Error creating matrix classes:", error);
        });
    });

    classifyImgsBtn.addEventListener('click', () => {
        resultsDiv.innerHTML = `Classifying images...`;
        classifyImgsBtn.disabled = true;
        fetch('/classify_imgs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ num_images: parseInt(numImagesClassInput.value) })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                thresholdSlider.disabled = false;
                widthInput.disabled = false;
                heightInput.disabled = false;
                settingsBtn.disabled = false;
                imageDisplayDiv.innerHTML = '';
                const correct = data.predictions[0];
                const incorrect = data.predictions[1];
                const total = correct + incorrect;
                // Round to the tenths place
                const perCorrect = Math.round((data.predictions[0] / total) * 1000) / 10;
                const perIncorrect = Math.round((data.predictions[1] / total) * 1000) / 10;
                resultsDiv.innerHTML = `
                    <p>${perCorrect}% (${correct}/${total}) of images were correctly classified with ${data.confidence}% confidence.</p>
                    <p>${perIncorrect}% (${incorrect}/${total}) of images were incorrectly classified.</p>
                `;
                if (data.img_paths.length > 0) {
                    resultsDiv.innerHTML += `<p>Images classified incorrectly:</p>`;
                    displayImages(data.img_paths);
                }
            } else {
                console.error("Classification failed:", data.message);
            }
        })
        .catch(error => {
            console.error("Error classifying directories:", error);
        });
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