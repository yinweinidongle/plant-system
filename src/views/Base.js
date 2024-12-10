import * as THREE from 'three'
import {CSS2DRenderer} from 'three/addons/renderers/CSS2DRenderer.js'
export default class Base{
    constructor(){
        this.scene = new THREE.Scene()
        
        const canvas = document.querySelector('#canvas');
        const width = window.innerWidth / 2; // 宽度为屏幕宽度的一半
        const height = window.innerHeight; // 高度为屏幕高度
        
        this.camera = new THREE.PerspectiveCamera(
            75,
            width/height,
            0.1,
            1000
        )
		
		this.cssRenderer = new CSS2DRenderer()
		this.cssRenderer.setSize(width, height)
		this.cssRenderer.domElement.style.position = 'absolute'
		this.cssRenderer.domElement.style.top = '0px'
		this.cssRenderer.domElement.style.right = '0px'
		canvas.appendChild(this.cssRenderer.domElement)
		this.cssRenderer.domElement.style.pointerEvents = 'none';
		
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            canvas: canvas
        })
        this.renderer.setSize(width, height)
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio,2))
        this.renderer.setClearColor('#262837')
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    }

    update(){
        this.renderer.render(this.scene,this.camera)
		this.cssRenderer.render(this.scene,this.camera)
    }
    
    //自适应
    resize(){
        const width = window.innerWidth / 2;
        const height = window.innerHeight;
        this.camera.aspect = width/height
        this.camera.updateProjectionMatrix()
        this.renderer.setSize(width, height)
        this.cssRenderer.setSize(width, height)
    }

    addAmbientLight(intensity=0.5,color=0xffffff){
        const light = new THREE.AmbientLight(color,intensity)
        this.scene.add(light)
    }

    addDirectionalLight(intensity=1,color=0xffffff){
        const derectLight = new THREE.DirectionalLight(color,intensity)
        derectLight.castShadow = true; 
        this.scene.add(derectLight)
    }
}