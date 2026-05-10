import { Canvas } from "@react-three/fiber";
import { Float } from "@react-three/drei";

export function FloatingIsland() {
  return (
    <Canvas camera={{ position: [0, 0, 4], fov: 50 }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[3, 3, 3]} intensity={1} />
      <Float speed={2} rotationIntensity={0.4} floatIntensity={0.8}>
        <mesh>
          <cylinderGeometry args={[1.5, 2, 0.4, 32]} />
          <meshStandardMaterial color="#4ade80" roughness={0.9} />
        </mesh>
        <mesh position={[0, 0.6, 0]}>
          <coneGeometry args={[0.4, 1.2, 8]} />
          <meshStandardMaterial color="#16a34a" />
        </mesh>
      </Float>
    </Canvas>
  );
}
