var malList;
var FINISHED = 2;
var ONGOING = 1;
var NOTAIRED = 3;

watching = 1
completed = 2
on_hold = 3
dropped = 4
plan_to_watch = 6


var container;
var scene;


var parent1;

$(document).ready(function() {
    malList = $("#visual").data("list");
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
    //geometry = new THREE.SphereGeometry(150, 5, 5); //.BoxGeometry(200, 200, 200, 10, 10, 10);

    controls = new THREE.OrbitControls(camera);
    controls.rotateSpeed = 1.0;
    controls.zoomSpeed = 1.2;
    controls.panSpeed = 0.8;

    parent1 = new THREE.Object3D();
    generateSpheresForAnime();
    parent1.position.set(0, 0, 0);
    scene.add(parent1);

    //var geometry = new THREE.BoxGeometry(1, 1, 1);
    // var material = new THREE.MeshBasicMaterial({
    //     color: 0x56a0d3,
    //     emissive: new THREE.Color('rgb(23,23,23)'),
    //     shading: THREE.FlatShading,
    //     wireframeLinewidth: 30,
    //     wireframe: true
    // });

    // var material = new THREE.LineBasicMaterial({
    //     color: 0x56a0d3,
    //     linewidth: 30,
    //     linecap: 'round', //ignored by WebGLRenderer
    //     linejoin: 'round', //ignored by WebGLRenderer
    //     wireframe: true
    // });

    //new THREE.MeshBasicMaterial({ color: 0x56a0d3, wireframe: true });
    //shape = new THREE.Mesh(geometry, material);
    //scene.add(shape);
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

function generateSpheresForAnime() {
    var finishedColor = new THREE.Color("rgb(255,255,255)");


    for (var i = 0; i < malList.length; i++) {
        var animeData = malList[i];
        if (animeData["airing_status"] == FINISHED) {
            let sphere = createSphere(200, 5, 5, finishedColor, 50, 50);
            parent1.add(sphere);
        } else if (animeData["airing_status"] == ONGOING) {

        } else if (animeData["airing_status"] == NOTAIRED) {

        }
        //var geometry = new THREE.SphereGeometry(150, 5, 5); //.BoxGeometry(200, 200, 200, 10, 10, 10);
    }
    //scene.add(parent1);
    console.log(parent1);

}

function createSphere(radius, wSegments, hSegments, color, x, y) {
    var sphereGeometry = new THREE.SphereGeometry(radius, wSegments, hSegments); //new THREE.DodecahedronGeometry(radius); //THREE.BoxGeometry(20, 20, 20, 10, 10, 10);//
    var sphereMaterial = new THREE.MeshLambertMaterial({ color: color, wireframe: true });

    var sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    sphere.position.x = x;
    sphere.position.y = y;

    return sphere;
}

// function generateParticles(coords, radius, wSegments = 8, hSegments = 6, color = sphereColor) {
//     var parent = new THREE.Object3D();
//     for (var i = 0; i < coords.length; i++) {
//         let coord = coords[i];
//         var sphereGeometry = new THREE.SphereGeometry(radius, wSegments, hSegments); //new THREE.DodecahedronGeometry(radius); //THREE.BoxGeometry(20, 20, 20, 10, 10, 10);//
//         var sphereMaterial = new THREE.MeshLambertMaterial({ color: color, wireframe: true });

//         var sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
//         sphere.position.x = coord[0];
//         sphere.position.y = coord[1];
//         parent.add(sphere);
//     }
//     return parent;
// }