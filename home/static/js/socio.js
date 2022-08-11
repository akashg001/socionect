
const allStories = [
    {
      thumbUrl: "../images/1-thumb.png",
      imageUrl: "../images/1.png",
      title: "Anuskha Sharma",
    },
  
    {
      thumbUrl: "2-thumb.png",
      imageUrl: "2.png",
      title: "Akash Gupta",
    },
  
    {
      thumbUrl: "3-thumb.png",
      imageUrl: "3.png",
      title: "Sunaina",
    },
  
    {
      thumbUrl: "4-thumb.png",
      imageUrl: "4.png",
      title: "Gourav Mishra",
    },
  
    {
      thumbUrl: "5-thumb.png",
      imageUrl: "5.png",
      title: "Abhijeet Singh",
    },
  
    {
      thumbUrl: "6-thumb.png",
      imageUrl: "6.png",
      title: "Preeti singh",
    },
  
    {
      thumbUrl: "7-thumb.png",
      imageUrl: "7.png",
      title: "Deepika Singh",
    },
  
    {
      thumbUrl: "8-thumb.png",
      imageUrl: "8.png",
      title: "Vishal kumar",
    },
  ];
  
  const storiesContainer = document.querySelector(".stories-container");
  const storyFull = document.querySelector(".story-full");
  const storyFullImage = document.querySelector(".story-full img");
  const storyFullTitle = document.querySelector(".story-full .title");
  const closeBtn = document.querySelector(".story-full .close-btn");
  const leftArrow = document.querySelector(".story-full .left-arrow");
  const rightArrow = document.querySelector(".story-full .right-arrow");
  
  let currentIndex = 0;
  let timer;
  
  allStories.forEach((s, i) => {
    const content = document.createElement("div");
    content.classList.add("content");
  
    const img = document.createElement("img");
    img.setAttribute("src", s.thumbUrl);
  
    storiesContainer.appendChild(content);
    content.appendChild(img);
  
    content.addEventListener("click", () => {
      currentIndex = i;
      storyFull.classList.add("active");
      storyFullImage.setAttribute("src", s.imageUrl);
  
      if (!s.title) {
        storyFullTitle.style.display = "none";
      } else {
        storyFullTitle.style.display = "block";
        storyFullTitle.innerHTML = s.title;
      }
  
      clearInterval(timer);
      timer = setInterval(nextStory, 5000);
    });
  });
  
  closeBtn.addEventListener("click", () => {
    storyFull.classList.remove("active");
  });
  
  leftArrow.addEventListener("click", () => {
    if (currentIndex > 0) {
      currentIndex -= 1;
  
      storyFullImage.setAttribute("src", allStories[currentIndex].imageUrl);
  
      if (!allStories[currentIndex].title) {
        storyFullTitle.style.display = "none";
      } else {
        storyFullTitle.style.display = "block";
        storyFullTitle.innerHTML = allStories[currentIndex].title;
      }
  
      clearInterval(timer);
      timer = setInterval(nextStory, 5000);
    }
  });
  
  const nextStory = () => {
    if (currentIndex < allStories.length - 1) {
      currentIndex += 1;
  
      storyFullImage.setAttribute("src", allStories[currentIndex].imageUrl);
  
      if (!allStories[currentIndex].title) {
        storyFullTitle.style.display = "none";
      } else {
        storyFullTitle.style.display = "block";
        storyFullTitle.innerHTML = allStories[currentIndex].title;
      }
    }
  };
  
  rightArrow.addEventListener("click", () => {
    nextStory();
    clearInterval(timer);
    timer = setInterval(nextStory, 2000);
  });
  
  const burger = document.querySelector(".burger");
  const navlist = document.querySelector(".left");
  const story = document.querySelector(".stories-container");
  const navslider = () =>{
    burger.addEventListener('click', () =>{
      console.log("clicked");
      navlist.classList.toggle("newactive");
      story.classList.toggle("none");
    });
    }
    
    navslider();