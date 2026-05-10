import { Suspense, lazy } from "react";
import { Canvas } from "@react-three/fiber";
import { Stars, OrbitControls } from "@react-three/drei";
import { Spinner } from "@/components/ui/Spinner";

const Globe = lazy(() => import("./GlobeScene").then((m) => ({ default: m.GlobeMesh })));

export function GlobeScene() {
  return (
    <div className="h-full w-full">
      <Suspense
        fallback={
          <div className="flex h-full items-center justify-center">
            <Spinner size="lg" />
          </div>
        }
      >
        <Canvas camera={{ position: [0, 0, 3.5], fov: 45 }}>
          <ambientLight intensity={0.4} />
          <directionalLight position={[5, 3, 5]} intensity={1.2} />
          <Stars radius={100} depth={50} count={3000} factor={4} />
          <Globe />
          <OrbitControls
            enableZoom={false}
            autoRotate
            autoRotateSpeed={0.5}
          />
        </Canvas>
      </Suspense>
    </div>
  );
}

export function GlobeMesh() {
  return (
    <mesh>
      <sphereGeometry args={[1.5, 64, 64]} />
      <meshStandardMaterial color="#1d4ed8" wireframe={false} roughness={0.8} />
    </mesh>
  );
}
