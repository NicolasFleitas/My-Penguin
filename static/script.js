// const frames = [
//   '/static/hearts.png',
//   '/static/hearts.png',
//   '/static/hearts.png',
//   '/static/hearts.png',
//   '/static/hearts.png',
// ];

// let currentFrame = 0;
// let imagesShown = 0;

// document.getElementById('taskForm').addEventListener('submit', (event) => {
//   event.preventDefault();

//   const input = document.getElementById('inputMessage');
//   const message = input.value.trim();
//   if (message === "") return;

//   fetch('/button-click', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ message }),
//   })
//   .then(response => response.text())
//   .then(() => {
//     const messagesContainer = document.getElementById('messagesContainer');

//     const taskDiv = document.createElement('div');
//     taskDiv.style.display = 'flex';
//     taskDiv.style.alignItems = 'center';
//     taskDiv.style.marginBottom = '8px';

//     const taskText = document.createElement('span');
//     taskText.textContent = message;
//     taskText.style.flexGrow = '1';

//     const taskButton = document.createElement('button');
//     taskButton.textContent = 'Completar';
//     taskButton.style.marginLeft = '10px';

//     taskButton.addEventListener('click', () => {
//       // Remove the task from the list
//       taskDiv.remove();

//       // Add a heart only if less than 5 hearts shown
//       if (imagesShown < 5) {
//         const heartsContainer = document.getElementById('heartscontainers');
//         const img = document.createElement('img');
//         img.src = frames[currentFrame];
//         img.alt = 'Heart animation frame';
//         img.style.marginRight = '5px';
//         heartsContainer.appendChild(img);

//         currentFrame = (currentFrame + 1) % frames.length;
//         imagesShown++;
//       }
//     });

//     taskDiv.appendChild(taskText);
//     taskDiv.appendChild(taskButton);
//     messagesContainer.appendChild(taskDiv);

//     input.value = '';
//   })
//   .catch(() => {
//     alert('Error sending message');
//   });
// });

