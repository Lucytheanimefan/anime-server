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
    var light = new THREE.HemisphereLight(0xffbf67, 0x15c6ff); //new THREE.PointLight(0xffffff, 1, 100);
    scene.add(light);
    container = document.getElementById("malVisual");
    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);
    geometry = new THREE.SphereGeometry(150, 5, 5); //.BoxGeometry(200, 200, 200, 10, 10, 10);

    controls = new THREE.OrbitControls(camera);
    controls.rotateSpeed = 1.0;
    controls.zoomSpeed = 1.2;
    controls.panSpeed = 0.8;

    generateSpheresForAnime();
    //parent1.position.set(0, 0, 0);

    console.log("Add to scene");


}

// TODO: speed not being used
function render(speed) {
    animationID = requestAnimationFrame(function() {
        render(speed);
    });
    // shape.rotation.x += increment;
    // shape.rotation.y += increment;
    //increment += speed;
    TWEEN.update();
    controls.update();
    renderer.render(scene, camera);
};

function generateSpheresForAnime() {
    var finishedColor = new THREE.Color("rgb(255,255,255)");
    parent1 = new THREE.Object3D();
    for (var i = 0; i < malList.length; i++) {
        var animeData = malList[i];
        // Maybe should base this on if user completed instead of if user has alreadu
        if (animeData["airing_status"] == FINISHED) {
        	var score = animeData["user_score"];
            var rad = score; // * 100;
            var seg = rad;
            var x = animeData["total_episodes"];
            var y = animeData["watched_episodes"] * 10;
            var z = Math.pow(score, 3)

            var sprite = makeTextSprite(animeData["title"], { fontsize: 20, borderThickness: 0.5,borderColor: { r: 255, g: 0, b: 0, a: 1.0 }, backgroundColor: { r: 255, g: 100, b: 100, a: 0.8 } });
            sprite.position.set(x,y,z);
            var sphere = createSphere(rad, seg, seg, finishedColor, x, y, z);
            //sphere.material.color = finishedColor;
            //sphere.material.color = new THREE.Color( 'skyblue' );
            //.material.color.set(genreColor);
            //

            // Set sphere on orbit - let's not do this for now
            // var speed = 10;
            // var tilt = Math.PI / 2;

            // var orbitContainer = new THREE.Object3D();
            // orbitContainer.rotation.z = tilt;

            // var orbit = new THREE.Object3D();

            // orbit.add(sphere);

            // var tween = new TWEEN.Tween(orbit.rotation).to({ z: '+' + (Math.PI * 2) }, 10000 / speed);
            // tween.onComplete(function() {
            // 	console.log("Tween on complete called");
            //     orbit.rotation.y = 0;
            //     tween.start();
            // });
            // tween.start();

            // //console.log("Start tween");
            // orbitContainer.add(orbit);
            //scene.add(orbitContainer);
            //parent1.add(orbitContainer);
            parent1.add(sphere);
            parent1.add(sprite);
        } else if (animeData["airing_status"] == ONGOING) {

        } else if (animeData["airing_status"] == NOTAIRED) {

        }
        //var geometry = new THREE.SphereGeometry(150, 5, 5); //.BoxGeometry(200, 200, 200, 10, 10, 10);
        scene.add(parent1);
    }

    console.log("new parent1");
    console.log(parent1);
    //scene.add(parent1);

}

function createSphere(radius, wSegments, hSegments, color = 0x56a0d3, x, y, z) {
    var sphereGeometry = new THREE.SphereGeometry(radius, wSegments, hSegments); //new THREE.DodecahedronGeometry(radius); //THREE.BoxGeometry(20, 20, 20, 10, 10, 10);//
    var sphereMaterial = new THREE.MeshLambertMaterial({ color: color, wireframe: true });
    //sphereMaterial.color.setHex(Math.random() * 0xffffff);

    var sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    sphere.position.x = x;
    sphere.position.y = y;
    sphere.position.z = z;

    return sphere;
}

function makeTextSprite(message, parameters, textColor="rgba(255, 255, 255, 1.0)") {
    if (parameters === undefined) parameters = {};

    var fontface = parameters.hasOwnProperty("fontface") ?
        parameters["fontface"] : "Arial";

    var fontsize = parameters.hasOwnProperty("fontsize") ?
        parameters["fontsize"] : 18;

    var borderThickness = parameters.hasOwnProperty("borderThickness") ?
        parameters["borderThickness"] : 4;

    var borderColor = parameters.hasOwnProperty("borderColor") ?
        parameters["borderColor"] : { r: 0, g: 0, b: 0, a: 1.0 };

    var backgroundColor = parameters.hasOwnProperty("backgroundColor") ?
        parameters["backgroundColor"] : { r: 255, g: 255, b: 255, a: 1.0 };
    //var spriteAlignment = THREE.SpriteAlignment.topLeft;

    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    context.font = "Bold " + fontsize + "px " + fontface;

    // get size data (height depends only on font size)
    var metrics = context.measureText(message);
    var textWidth = metrics.width;

    // background color
    context.fillStyle = "rgba(" + backgroundColor.r + "," + backgroundColor.g + "," +
        backgroundColor.b + "," + backgroundColor.a + ")";
    // border color
    context.strokeStyle = "rgba(" + borderColor.r + "," + borderColor.g + "," +
        borderColor.b + "," + borderColor.a + ")";
    context.lineWidth = borderThickness;
    //roundRect(context, borderThickness / 2, borderThickness / 2, textWidth + borderThickness, fontsize * 1.4 + borderThickness, 6);
    // 1.4 is extra height factor for text below baseline: g,j,p,q.

    // text color
    context.fillStyle = textColor;//"rgba(100, 100, 100, 1.0)";
    context.fillText(message, borderThickness, fontsize + borderThickness);

    // canvas contents will be used for a texture
    var texture = new THREE.Texture(canvas)
    texture.needsUpdate = true;
    var spriteMaterial = new THREE.SpriteMaterial({ map: texture, useScreenCoordinates: false});//, alignment: spriteAlignment });
    var sprite = new THREE.Sprite(spriteMaterial);
    sprite.scale.set(100, 50, 1.0);
    return sprite;
}