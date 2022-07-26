// https://marcbruederlin.github.io/particles.js/
window.onload = function() {
  Particles.init({
    selector: '.background',
    speed:.5,
    connectParticles:true,
    color: "#7CB9E8",
  });
};

function setActiveNavLink(id){
  var element=document.getElementById(id);
  if (element != null){
    element.className+=" nav-link-active";
  }
  else{
    console.log("setActiveNavLink could not find the id to set active(?)")    
  }
  console.log("ran setActiveNavLink")
}
