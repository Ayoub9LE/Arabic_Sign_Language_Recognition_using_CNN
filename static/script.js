// Get DOM elements
const imageUpload = document.getElementById('image-upload');
const uploadLabel = document.getElementById('upload-label');
const uploadedCanvas = document.getElementById('uploaded-canvas');
const predictBtn = document.getElementById('predict-btn');
const output = document.getElementById('output');
const textToVoiceBtn = document.getElementById('text-to-voice-btn');

// Image upload event listener
imageUpload.addEventListener('change', (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = (e) => {
    const img = new Image();
    img.src = e.target.result;

    img.onload = () => {
      uploadedCanvas.width = img.width;
      uploadedCanvas.height = img.height;
      const context = uploadedCanvas.getContext('2d');
      context.drawImage(img, 0, 0);
      uploadedCanvas.style.display = 'block';
    };
  };

  reader.readAsDataURL(file);
});

// ...

// Predict button click event listener
// ...

// Predict button click event listener
predictBtn.addEventListener('click', () => {
  const file = imageUpload.files[0];
  const formData = new FormData();
  formData.append('image', file);

  fetch('/predict', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      const prediction = data.prediction; // Updated key here
      output.value = prediction;
    })
    .catch(error => {
      console.error('Error:', error);
    });
});

// ...

// ...



textToVoiceBtn.addEventListener('click', () => {
  const text = output.value;
  if (!text) {
    return;
  }

  // Make an HTTP request to Flask for text-to-speech
  fetch('/generate_audio', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: text })
  })
    .then(response => response.json())
    .then(data => {
      const audioUrl = data.audio_url;
      console.log(audioUrl);  // Log the URL for debugging

      // Create an audio element and set the source to the generated audio file
      const audio = new Audio(audioUrl);
      audio.oncanplaythrough = () => {
        // When audio is ready to play, play it
        audio.play();
      };
      audio.onerror = (error) => {
        console.error('Error:', error);
      };
    })
    .catch(error => {
      console.error('Error:', error);
    });
});





