$(document).ready(function() {
    var malList = $("#visual").data("list");
    console.log(malList);
    init3d();
    render(0.000001);
})

function init3d() {
    scene = new THREE.Scene();
    //scene.background = new THREE.Color(0xffffff);
    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.y = 150;
    camera.position.z = 500;
    camera.lookAt(scene.position);
    container = document.getElementById("visual");
    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);
    geometry = new THREE.SphereGeometry(150, 5, 5); //.BoxGeometry(200, 200, 200, 10, 10, 10);

    controls = new THREE.OrbitControls(camera);
    controls.rotateSpeed = 1.0;
    controls.zoomSpeed = 1.2;
    controls.panSpeed = 0.8;

    //var geometry = new THREE.BoxGeometry(1, 1, 1);
    var material = new THREE.MeshBasicMaterial({
        color: 0x56a0d3,
        emissive: new THREE.Color('rgb(23,23,23)'),
        shading: THREE.FlatShading,
        wireframeLinewidth: 30,
        wireframe: true
    });

    // var material = new THREE.LineBasicMaterial({
    //     color: 0x56a0d3,
    //     linewidth: 30,
    //     linecap: 'round', //ignored by WebGLRenderer
    //     linejoin: 'round', //ignored by WebGLRenderer
    //     wireframe: true
    // });

    //new THREE.MeshBasicMaterial({ color: 0x56a0d3, wireframe: true });
    shape = new THREE.Mesh(geometry, material);
    scene.add(shape);
}

function render(speed) {
    animationID = requestAnimationFrame(function() {
        render(speed);
    });
    // shape.rotation.x += increment;
    // shape.rotation.y += increment;
    //increment += speed;
    controls.update();
    renderer.render(scene, camera);
};