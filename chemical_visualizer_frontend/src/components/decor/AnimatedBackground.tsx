import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Stars, Float } from '@react-three/drei';
import * as THREE from 'three';

function FloatingParticles() {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.05;
      groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.1) * 0.1;
    }
  });

  return (
    <group ref={groupRef}>
      <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
      
      {/* Floating wireframe shapes */}
      <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
        <mesh position={[-5, 2, -5]}>
          <octahedronGeometry args={[1.5, 0]} />
          <meshBasicMaterial color="#00BCD4" wireframe />
        </mesh>
      </Float>

      <Float speed={1.5} rotationIntensity={0.3} floatIntensity={0.3}>
        <mesh position={[5, -2, -8]}>
          <torusGeometry args={[1, 0.3, 16, 100]} />
          <meshBasicMaterial color="#FF6B35" wireframe />
        </mesh>
      </Float>

      <Float speed={2.5} rotationIntensity={0.4} floatIntensity={0.6}>
        <mesh position={[0, 3, -10]}>
          <icosahedronGeometry args={[1, 0]} />
          <meshBasicMaterial color="#00BCD4" wireframe />
        </mesh>
      </Float>
    </group>
  );
}

export const AnimatedBackground = () => {
  return (
    <div className="fixed inset-0 -z-10 opacity-30">
      <Canvas camera={{ position: [0, 0, 5], fov: 75 }}>
        <ambientLight intensity={0.5} />
        <FloatingParticles />
      </Canvas>
    </div>
  );
};
