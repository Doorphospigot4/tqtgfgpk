"use client";

import maplibregl from "maplibre-gl";
import { useEffect, useRef } from "react";
import "maplibre-gl/dist/maplibre-gl.css";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const FALLBACK_STYLE = {
  version: 8 as const,
  sources: {
    osm: {
      type: "raster" as const,
      tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
      tileSize: 256,
      attribution: "© OpenStreetMap contributors",
    },
  },
  layers: [
    { id: "osm", type: "raster" as const, source: "osm" },
  ],
};

export default function ForecastMap({ day }: { day: number }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;
    const maptilerKey = process.env.NEXT_PUBLIC_MAPTILER_KEY;
    const style = maptilerKey
      ? `https://api.maptiler.com/maps/ocean/style.json?key=${maptilerKey}`
      : (FALLBACK_STYLE as unknown as maplibregl.StyleSpecification);

    const map = new maplibregl.Map({
      container: containerRef.current,
      style,
      center: [120.5, 24.0],
      zoom: 6,
    });
    mapRef.current = map;
    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    const layerId = "forecast-tiles";
    const sourceId = "forecast-src";

    const setupLayer = () => {
      if (map.getLayer(layerId)) map.removeLayer(layerId);
      if (map.getSource(sourceId)) map.removeSource(sourceId);

      map.addSource(sourceId, {
        type: "raster",
        tiles: [`${API}/tiles/{z}/{x}/{y}.png?day=${day}`],
        tileSize: 256,
      });
      map.addLayer({
        id: layerId,
        type: "raster",
        source: sourceId,
        paint: { "raster-opacity": 0.65 },
      });
    };

    if (map.isStyleLoaded()) {
      setupLayer();
    } else {
      map.once("load", setupLayer);
    }
  }, [day]);

  return <div ref={containerRef} className="w-full h-[calc(100vh-64px)]" />;
}
