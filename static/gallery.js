var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("photos");
  var dots = document.getElementsByClassName("demo");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  //slideIndex = (n % slides.length) + 1;
  for (i = 0; i < slides.length; i++) {
    //if(i== slideIndex){
    //  slides[slideIndex-1].style.display = "block";
    //}else{
      slides[i].style.display = "none";
    //}
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}