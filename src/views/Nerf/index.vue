<script setup>
import {onMounted} from "vue";

import {ref,reactive} from "vue";
import * as THREE from 'three'
import Base from "../Base";
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader.js';

import mqtt from "mqtt";

import axios from 'axios';


import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js';
import { OutlinePass } from 'three/examples/jsm/postprocessing/OutlinePass.js';
import { FXAAShader } from 'three/examples/jsm/shaders/FXAAShader.js';


import {GUI} from "three/examples/jsm/libs/lil-gui.module.min.js"
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js'
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js'
import {gsap} from 'gsap'
import * as TWEEN from '@tweenjs/tween.js';
import {CSS2DObject} from 'three/addons/renderers/CSS2DRenderer.js'

import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader.js';
import { Line2 } from 'three/examples/jsm/lines/Line2.js'
import { LineMaterial } from 'three/examples/jsm/lines/LineMaterial.js'
import { LineGeometry } from 'three/examples/jsm/lines/LineGeometry.js'

import { compute } from "../../api/record";

import { DoubleRightOutlined,DoubleLeftOutlined ,CloseOutlined} from '@ant-design/icons-vue';



let base,controls,client,gui,clock,object,material,group,drone,cylinder,loaderFlag,tractor,loaderTractorFlag,shaderMaterial,shaderCityMaterial,meshLand,pipeMaterial,loaderTractorFlag1;

const materials = [];
let parameters;

let mixer,portalLightMaterial,cubeTexture,holoFlag,robot;


let leaf0,grain0,showcase;

let robotOriginMaterial = new Map()

const data1 = ref(0.0)
const data2 = ref(0.0)
const data3 = ref(0.0)
const data4 = ref(0.0)
let distancePlace = ref(0.0);

const loading = ref(false)
const loadingSpin = ref(false)
let stopRotate = true

const parts = []

const glbs = []







let objInfo = reactive({
  "name":"叶子1",
  "width":"13cm",
  "length":"3cm",
  "area":"39cm²"
})

let filename = ref("leaf0 - Cloud.ply")


let showInfo = ref(false)

let showGrain = ref(false)




//麦穗数据
let arr_info = [

  {"name":"麦穗","count":"20","filename":"/demo1/grain0 - Cloud.ply"},
  {"name":"叶子1","width":"0.3cm","length":"10.6cm","area":"9.3cm²","filename":"/demo1/leaf0 - Cloud.ply"},
  {"name":"叶子2","width":"0.8cm","length":"16.7cm","area":"25.1cm²","filename":"/demo1/leaf1 - Cloud.ply"},
  {"name":"叶子3","width":"0.9cm","length":"21.1cm","area":"44.9cm²","filename":"/demo1/leaf2 - Cloud.ply"},
  {"name":"茎秆1","width":"0.8cm","length":"23.4cm","area":"28.0cm²","filename":"/demo1/stem0 - Cloud.ply"},

]


let arr_demo3 = [{"name":"麦穗","count":"29","filename":"/pcd_demo/demo3/grain0.ply"},
{"name":"麦穗","count":"18","filename":"/pcd_demo/demo3/grain1.ply"},
{"name":"麦穗","count":"45","filename":"/pcd_demo/demo3/grain2.ply"},
{"name":"叶子1","width":"0.4255cm","length":"8.0926cm","area":"5.3354cm²","filename":"/pcd_demo/demo3/leaf0.ply"},
{"name":"叶子2","width":"2.4131cm","length":"8.0926cm","area":"12.3466cm²","filename":"/pcd_demo/demo3/leaf1.ply"},
{"name":"叶子3","width":"0.2409cm","length":"3.6027cm","area":"0.505cm²","filename":"/pcd_demo/demo3/leaf2.ply"},
{"name":"叶子4","width":"0.3385cm","length":"7.6152cm","area":"4.6769cm²","filename":"/pcd_demo/demo3/leaf3.ply"},
{"name":"叶子5","width":"0.4164cm","length":"10.4487cm","area":"6.3229cm²","filename":"/pcd_demo/demo3/leaf4.ply"},
{"name":"叶子6","width":"0.3898cm","length":"12.281cm","area":"11.3758cm²","filename":"/pcd_demo/demo3/leaf5.ply"},
{"name":"茎秆0","width":"0.5896cm","length":"21.7409cm","area":"26.2885cm²","filename":"/pcd_demo/demo3/stem0.ply"},
{"name":"茎秆1","width":"0.7404cm","length":"13.1906cm","area":"16.1106cm²","filename":"/pcd_demo/demo3/stem1.ply"},
{"name":"茎秆2","width":"0.9724cm","length":"17.1723cm","area":"22.3211cm²","filename":"/pcd_demo/demo3/stem2.ply"}]

const urls = [
  
  "http://localhost:7008",
  "http://localhost:7008",
  "http://localhost:7008",
]


//初始化植物列表数据,名称,icon,时间,点云位置,子点云,缩放比例
let plantData = ref([
  {"id":1,"name":"第一盆","icon":"/wheat.png","scantime":"2024-11-24","file":"/plant_points/herb2 - Cloud.ply","scale":3,"children":arr_demo3,
    "url":urls[0],
    "code":"bx0001"
  },
  {"id":2,"name":"第二盆","icon":"/wheat.png","scantime":"2024-11-09","file":"/plant_points/point_cloud_20241023.ply","scale":10,"children":[],
    "url":urls[1],
    "code":"bx0002"
  },
  {"id":3,"name":"第三盆","icon":"/wheat.png","scantime":"2024-11-12","file":"/plant_points/point_cloud_wheat.ply","scale":3,"children":arr_info,
    "url":urls[2],
    "code":"bx0003"
  }
  
])


let url = ref(urls[0])




let composer, effectFXAA, outlinePass;
let selectedObjects = [];
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();


const materialLight = new THREE.PointsMaterial({color: 0xffffff, size: .01});

const materialLight01 = new THREE.PointsMaterial({color: 0xff0000, size: .01});

material = new THREE.PointsMaterial({vertexColors: true, size: .01});

const loader = new PLYLoader();

const groupWheat = new THREE.Group()

let activeIndex = ref(1)

let tabFlag = ref(false)
let showcaseFlag = false




onMounted(()=>{
    base = new Base()
    base.camera.position.z = 15
    base.camera.position.y = 0
    base.camera.updateProjectionMatrix()
    base.addAmbientLight(1,0xb9d5ff)
    base.addDirectionalLight(0.5,0xb9d5ff)
    controls = new OrbitControls(base.camera,base.renderer.domElement)
    clock = new THREE.Clock()
    window.addEventListener("resize",resize)
    //createBox();

    controls.maxPolarAngle = Math.PI / 2
    controls.minPolarAngle = Math.PI / 2
    controls.maxAzimuthAngle = Infinity
    controls.minAzimuthAngle = -Infinity

    

    // skybox

    const cubeTextureLoader = new THREE.CubeTextureLoader();
				cubeTextureLoader.setPath( '/skybox/' );

				cubeTexture = cubeTextureLoader.load( [
					"px.jpg", "nx.jpg",
					"py.jpg", "ny.jpg",
					"pz.jpg", "nz.jpg"
				] );

	//base.scene.background = cubeTexture;


  //point light
  const doorLight = new THREE.PointLight('#ff7d46',10,7)
    doorLight.position.set(0,10,0)
    doorLight.castShadow = true
    //base.scene.add(doorLight)


 

    const loaderGlb = new GLTFLoader();
    // Optional: Provide a DRACOLoader instance to decode compressed mesh data
    const dracoLoader = new DRACOLoader();
    //dracoLoader.setDecoderPath( '/examples/jsm/libs/draco/' );
    dracoLoader.setDecoderPath( '/draco/' )
    loaderGlb.setDRACOLoader( dracoLoader );
    // Load a glTF resource
    loaderGlb.load(
        "/white_round_exhibition_gallery.glb",
        function ( gltf ) {

            showcase = gltf.scene
            showcase.scale.set(1,1,1)
            showcase.position.x = 0;
            showcase.position.y = 0;
            showcase.position.z = 0;
           

            //base.scene.add(showcase)

        }
    );


  


    // light

    const ambientLight = new THREE.AmbientLight( 0xcccccc, 0.4 );
	base.scene.add( ambientLight );

				const directionalLight = new THREE.DirectionalLight( 0xffffff, 1 );
				directionalLight.position.set( - 1, 1, 1 );
				
				const directionalLightB  = new THREE.DirectionalLight( 0xffffff, 0.5 );
				
				directionalLightB.position.set(1,3,-3)
				
	base.scene.add( directionalLight );
	base.scene.add( directionalLightB );
	directionalLight.visible = true
	directionalLightB.visible = true


	
	 

  const rgbeLoader = new RGBELoader();



// rgbeLoader.load(
//   '/industrial_sunset_02_4k.hdr',
//   texture => {
//     const pmremGenerator = new THREE.PMREMGenerator( base.renderer );
//     pmremGenerator.compileEquirectangularShader();
//     const envMap = pmremGenerator.fromEquirectangular( texture ).texture;
//     base.scene.background = envMap;
//     base.scene.environment = envMap;
//     texture.dispose();
//     pmremGenerator.dispose();
//   },
//   undefined,
//   error => {
//     console.error( 'Error loading HDR texture', error );
//   }
// );







//默认首次加载第一条数据

const firstData = plantData.value[0]



if(firstData.children.length>0){

  //当存在子点云时，展示所有点云数据
  for(let i=0;i<firstData.children.length;i++){
    loader.load(firstData.children[i].filename, function (geometry) {
      geometry.computeVertexNormals();
      object = new THREE.Points(geometry, material);
      object.scale.set(firstData.scale,firstData.scale,firstData.scale)
      object.rotation.x = - Math.PI *0.5;
      loaderFlag = true
      let userData = firstData.children[i]
      object.userData.name = userData.name;
      if(i==0){
        object.userData.count = userData.count
      }else{

        object.userData.length = userData.length;
        object.userData.width = userData.width;
        object.userData.area = userData.area;
        object.userData.filename = userData.filename;
      }


      groupWheat.add(object)
    });
  }

}else{

  //当不存在子点云数据，直接加载
  loader.load(firstData.file, function (geometry) {
      geometry.computeVertexNormals();
      object = new THREE.Points(geometry, material);
      object.scale.set(firstData.scale,firstData.scale,firstData.scale)
      object.rotation.x = - Math.PI *0.5;
      loaderFlag = true
      let userData = firstData
      object.userData.name = firstData.name;


      //居中
      let box = new THREE.Box3();
      // box.expandByObject(this.model);
      box.expandByObject(object);
      // console.log('查看包围盒box3', box);
      //scaleV3表示包围盒长宽高尺寸
      let scaleV3 = new THREE.Vector3();
      // .getSize()计算包围盒长宽高尺寸
      box.getSize(scaleV3)
      // 查看控制台包围盒大小，辅助设置相机参数
      // console.log('查看包围盒尺寸', scaleV3);
      //scaleV3表示包围盒的几何体中心
      let center = new THREE.Vector3();
      // .getCenter()计算一个层级模型对应包围盒的几何体中心
      box.getCenter(center);
      // 查看控制台包围盒集合中心，作为lookAt()参数
      // console.log('查看几何中心', center);
      object.position.set(-center.x,-center.y,-center.z)

      
      groupWheat.add(object)
    });

}


glbs.push(groupWheat)
base.scene.add(...glbs)



//createBox()


        base.renderer.domElement.addEventListener( 'pointerdown', onPointerMove );

        function onPointerMove( event ) {

            if ( event.isPrimary === false ) return;

            // 只检测右半部分屏幕的点击
            if (event.clientX > window.innerWidth / 2) {
              mouse.x = ((event.clientX - window.innerWidth / 2) / (window.innerWidth / 2)) * 2 - 1;
            }
            mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1;

            checkIntersection();

        }

        function addSelectedObject( object ) {

           
            selectedObjects.push( object );

            console.log("length",selectedObjects.length)
            for(let i=0;i<selectedObjects.length;i++){
              selectedObjects[i].material = material
            }

            //selectedObjects = []

        }

        function checkIntersection() {

            raycaster.setFromCamera( mouse, base.camera );

            raycaster.params.Points.threshold = 0.01

            const intersects = raycaster.intersectObject( base.scene, true );

            if ( intersects.length > 0 ) {

              const selectedObject = intersects[ 0 ].object;
              if (selectedObject.type != 'Points') return;
              addSelectedObject( selectedObject );
              
              selectedObject.material = materialLight

              
              showInfo.value = false
              
              objInfo.name = selectedObject.userData.name
                if(selectedObject.userData.name == "麦穗"){
                  objInfo.count = selectedObject.userData.count

                  loadingSpin.value = true

                  setTimeout(function(){

                    
                    loadingSpin.value = false
                    showGrain = true
                    showInfo.value = true

                    },600)
                  

                }else{



                  filename.value = selectedObject.userData.filename

                  console.log("filename",filename.value)
                  loadingSpin.value = true

                  //computeAnalysis()

                  let delay = Math.random()*0.5

                  showGrain = false

                  objInfo.name = selectedObject.userData.name
                  objInfo.width = selectedObject.userData.width
                  objInfo.length = selectedObject.userData.length
                  objInfo.area = selectedObject.userData.area

                  setTimeout(function(){

                    

                    loadingSpin.value = false

                    showInfo.value = true

                  },delay*1000)
                  
                  
                }
                
                

                
                
                

            } else {

                // outlinePass.selectedObjects = [];

            }

        }



	

	

	
	

	


	
	
	
	
	
	
  

    
    


 
  

    

	
	
   

   

    update()







});



function createBox(){
    const geometry = new THREE.BoxGeometry(1,1,1)
    const materail = new THREE.MeshBasicMaterial({color:0x00ff00})
    const cube = new THREE.Mesh(geometry,materail)
    base.scene.add(cube)
}






function changeRotate(){
 
  stopRotate = !stopRotate
}


//点击，加载点云数据

function showPoints(id){

  url.value = plantData.value[id-1].url

  loadingSpin.value = true

  

  activeIndex.value = id
  
  const obj =  plantData.value.filter(item => item["id"] == id);

  //清除场景中所有物体
  groupWheat.remove(...groupWheat.children);  // for removing all objects from the group 
  //groupWheat.matrixAutoUpdate = true;
  for(let i=0;i<glbs.length;i++){
    
    base.scene.remove(glbs[i])
  }

  const firstData0 = obj[0]

  //重新加载点云
  if(firstData0.children.length>0){

    

    //当存在子点云时，展示所有点云数据
    for(let i=0;i<firstData0.children.length;i++){
      
      loadingSpin.value = true
      loader.load(firstData0.children[i].filename, function (geometry) {
        geometry.computeVertexNormals();
        object = new THREE.Points(geometry, material);
        object.scale.set(firstData0.scale,firstData0.scale,firstData0.scale)
        object.rotation.x = - Math.PI *0.5;
        loaderFlag = true
        let userData = firstData0.children[i]
        object.userData.name = userData.name;
        if(i==0){
          object.userData.count = userData.count
        }else{

          object.userData.length = userData.length;
          object.userData.width = userData.width;
          object.userData.area = userData.area;
          object.userData.filename = userData.filename;
        }

       
        groupWheat.add(object)

        loadingSpin.value = false

      });

      
      
    }

    }else{

    //当不存在子点云数据，直接加载
    loader.load(firstData0.file, function (geometry) {
        
        geometry.computeVertexNormals();
        object = new THREE.Points(geometry, material);
        object.scale.set(firstData0.scale,firstData0.scale,firstData0.scale)
        object.rotation.x = - Math.PI *0.5;
        loaderFlag = true
        let userData = firstData0
        object.userData.name = firstData0.name;

        //居中
        let box = new THREE.Box3();
        // box.expandByObject(this.model);
        box.expandByObject(object);
        // console.log('查看包围盒box3', box);
        //scaleV3表示包围盒长宽高尺寸
        let scaleV3 = new THREE.Vector3();
        // .getSize()计算包围盒长宽高尺寸
        box.getSize(scaleV3)
        // 查看控制台包围盒大小，辅助设置相机参数
        // console.log('查看包围盒尺寸', scaleV3);
        //scaleV3表示包围盒的几何体中心
        let center = new THREE.Vector3();
        // .getCenter()计算一个层级模型对应包围盒的几何体中心
        box.getCenter(center);
        // 查看控制台包围盒集合中心，作为lookAt()参数
        // console.log('查看几何中心', center);
        object.position.set(-center.x,-center.y,-center.z)
        
        groupWheat.add(object)

        loadingSpin.value = false
      });

    }


    

    glbs.push(groupWheat)

    base.scene.add(...glbs)

    


  
}


//点击展开/收缩leftbar
function showList(){
  tabFlag.value = !tabFlag.value
}


//显示隐藏展台
function changeShowcase(){
  showcaseFlag = !showcaseFlag

  if(showcaseFlag){
    base.scene.add(showcase)
  }else{
    base.scene.remove(showcase)
  }
}





let message = ref("")
const computeAnalysis01 = async () => {
  let response = await axios.get('http://localhost:5000/api/plyAnalysis?filePath='+filename.value)


}


//模拟数据，直接计算长宽、面积
async function computeAnalysis() {
      let params = {
        filePath: filename.value,
      };
      let res = await compute(params)
      objInfo.width = res.width.toFixed(2)
      objInfo.length = res.length.toFixed(2)
      objInfo.area = res.area.toFixed(2)

      loadingSpin.value = false

      showInfo.value = true


      
}


function closeInfo(){
  showInfo.value = false
}






function update() {

  
	const elapsedTime = clock.getElapsedTime()*0.5

  if(loaderFlag && stopRotate){
    groupWheat.rotation.y += 0.01
  }

    

    requestAnimationFrame(update)
    base.update()
    controls.update()
	TWEEN.update()
    
}

function resize(){
    base.resize();
}

</script>

<template>

  <!--<div class="distance" style="position:absolute;left:50%;top:15%;color:#fff;transform: translateX(-50%);">长度：{{distancePlace.toFixed(2)}}</div>-->
	<div class="camera">

		<!-- <div class="camera-a" @click="changeCamera">视角</div> -->

    <div class="camera-a" @click="changeRotate">旋转</div>

    <div class="camera-a" @click="showList">列表</div>

    <div class="camera-a" @click="changeShowcase">展台</div>

    

	</div>


  <div  :class="tabFlag  ? 'left-bar-hide' : 'left-bar-show' ">

    

    <div class="plant-list">

      

      <div :class="activeIndex == item.id ? 'list-item list-item-active' : 'list-item' " v-for=" (item,index) in plantData" :key="item.id" @click="showPoints(item.id)">
        <div class="it-col">
          <img class="it-img" :src="item.icon" alt="">
        </div>
        <div class="it-col">
          <div class="col-title">{{ item.name }}</div>
          <div class="col-content">扫描时间：{{ item.scantime }}</div>
          <div class="col-content">ID：{{ item.code }}</div>
        </div>
      </div>

    </div>

  </div>

  


    <div id="left-section">
        <iframe :src="url"></iframe>
         <!-- <img src="../../assets/points.png" alt=""> -->
    </div>
    <div id="right-section">
        <canvas id="canvas"></canvas>
    </div>



 


  <div class="compute-info" v-if="showInfo">
    
    <div class="compute-sub">

      <div class="info-title">{{ objInfo.name }}</div>

      <div class="info-content" v-if="showGrain && objInfo.count">穗粒数：{{ objInfo.count }}</div>
      <div class="info-content" v-if="!showGrain && objInfo.length">叶长：{{ objInfo.length }}</div>
      <div class="info-content" v-if="!showGrain && objInfo.width">叶宽：{{ objInfo.width }}</div>
      <div class="info-content" v-if="!showGrain && objInfo.width">叶片面积：{{ objInfo.area }}</div>

      <span @click="closeInfo"><CloseOutlined /></span>

    </div>
    
    
  </div>


  <div class="load-spin" v-if="loading === true">
    <a-spin style="transform:scale(3);"/>
  </div>

  <a-spin v-if="loadingSpin"  style="position: absolute;top:50%;left:50%;transform: translateX(-50%) scale(2);"/>
  
  
</template>

<style scoped>

/* 定制整个滚动条 */
::-webkit-scrollbar {
  width: 12px;  /* 滚动条宽度 */
}
 
/* 定制滚动条轨道 */
::-webkit-scrollbar-track {
  background: #f1f1f1; /* 轨道颜色 */
}
 
/* 定制滚动条的滑块（thumb） */
::-webkit-scrollbar-thumb {
  background: #888; /* 滑块颜色 */
}
 
/* 当鼠标悬停在滑块上 */
::-webkit-scrollbar-thumb:hover {
  background: #555; /* 滑块悬停颜色 */
}
html, body {
  margin: 0;
  padding: 0;
  overflow: hidden;
  height: 100vh;
}


#left-section {
  width: 50vw;
  height: 100vh;
  overflow: hidden;
  float: left;
  border-right:10px solid #fff ;
}

#right-section {
  width: 50vw; 
  height: 100vh;
  overflow: hidden;
  float: right;
}

iframe {
  width: 100%;
  height: 100%;
  border: none;
}

canvas {
  width: 100%;
  height: 100%;
  display: block;
}



.loading-bar{
    position:absolute;
    top:50%;
    width:100%;
    height:2px;
    background-color: #ffffff;
    transform: scaleX(0);
    transform-origin: top left;
    transition:transform 0.5s;
    will-change: transform;
}

.loading-bar.ended{
    transform-origin: top right;
    transition:transform 1.5s ease-in-out;
}
.camera{position:absolute;top:0;right:0;padding:10px;}
.camera>div{margin-right:10px;background:#333;color:#fff;padding:5px 10px;border:1px solid #fff;border-radius:2px;margin-top:10px;cursor: pointer;float:left;}

.camera>div:hover{background:#fff;color: #333;;padding:5px 10px;border:1px solid #fff;border-radius:2px;margin-top:10px;cursor: pointer;}



.left-bar-hide{
  position: absolute;
  bottom: 0px;
  /* width: 90%; */
  left: 50%;
  transform: translateX(-50%);
  transform-origin: center center;
  animation: barhide 1.4s ease-in-out;
  animation-fill-mode: forwards;
  
}

.left-bar-show{
  position: absolute;
  bottom: 0px;
  /* width: 90%; */
  left: 50%;
  transform: translateX(-50%);
  transform-origin: center center;
  animation: barshow 1.4s ease-in-out;
  animation-fill-mode: forwards;
  
}

@keyframes barhide {
  0% {
    transform: translateX(-50%) scale(1);
  }
  100% {
    transform: translateX(-50%) scale(0);
  }
}

@keyframes barshow {
  0% {
    transform: translateX(-50%) scale(0);
  }
  100% {
    transform: translateX(-50%) scale(1);
  }
}



.tab-pin:hover{
  border: 1px solid #fff;
  cursor: pointer;
}



.plant-list{
  
  width:100%;
  height:100%;
  border:1px solid #fff;
  display: flex;
  flex-direction: row;
  color:#fff;
  border-radius: 3px;
  overflow-y: hidden;
  background-color: #555;
}

.list-item{
  display: flex;
  flex-direction: row;
  height:200px;
  border-right: #fff 1px solid;
}

.list-item:hover{
  background-color: cadetblue;

  .it-img{transform: scale(1.2);}

}



.list-item-active{
  background-color: cadetblue;
  .it-img{transform: scale(1.2);}

}

.it-col:nth-child(1){
 flex:2;
}
.it-col:nth-child(2){
 flex:4;
}
.it-img{width:100%;height:100%;}
.col-title{height:100px;line-height: 100px;font-size: 30px;font-weight: 700;}
.col-content{height:40px;line-height: 40px;font-size: 20px;color:beige;}



.video1{position:absolute;top:10px;right:0;padding:10px;width:500px;height:300px;background-color: #fff;}

.video2{position:absolute;top:320px;right:0;padding:10px;width:500px;height:300px;background-color: #fff;}

.compute-info{position:absolute;top:100px;right:1%;padding:10px;width:200px;color:#fff;border: 1px solid #fff;border-radius: 5px;}
.compute-sub{width:200px;position: relative;}
.compute-sub>div{padding: 5px 10px;}
.compute-sub>div.info-title{font-size: large;color:antiquewhite;text-shadow:  0 0 12px yellow;}

.compute-sub>span{position: absolute;top:-20px;right:0;display: inline-block;width:30px;height:30px;text-align: center;border-radius: 50%;border: 1px solid #fff;font-size: 20px;background-color: #333;cursor: pointer;line-height: 30px;}

.compute-sub>span:hover{
  background-color: #fff;
  color:#333;
}

#video-player{width:100%;height:100%;}

.remote-ctl{
  position:absolute;top:180px;left:0;padding:20px;
  color:#fff;
  border: 1px solid #fff;
}

.remote-ctl>div{
  margin-top:20px;
  color:#fff;
}

.remote-ctl>div span{
  display: inline-block;
  width:50px;
}

.remote-video{
  position:absolute;top:100px;left:0;padding:20px;
  color:#fff;
  border: 1px solid #fff;
}

.load-spin{
  position:absolute;
  top:50%;
  left:50%;
}

.remote-nerf{
  position:absolute;top:230px;left:0;padding:20px;width:550px;
  color:#fff;
  border: 1px solid #fff;
}

.remote-tool{
  position:absolute;top:330px;left:0;padding:20px;width:380px;
  color:#fff;
  border: 1px solid #fff;
}




</style>