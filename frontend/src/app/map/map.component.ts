import { Component, OnInit } from '@angular/core';
import * as L from 'leaflet';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-map',
  standalone: true,
  imports: [],
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss'],
})
export class MapComponent implements OnInit {
  private map!: L.Map;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.initMap();
    this.loadRoads();
  }

  private initMap(): void {
    // Initialize the map and set its view to a specific geographical coordinates
    this.map = L.map('map').setView([52.237049, 21.017532], 13);

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap contributors',
    }).addTo(this.map);
  }

  private loadRoads(): void {
    this.http.get<{ type: string; features: any[] }>('http://localhost:8000/api/river/rivers/').subscribe((data) => {
      this.addRoadsToMap(data.features);
    });
  }

  private addRoadsToMap(roadFeatures: any[]): void {
    roadFeatures.forEach((feature) => {
      const coordinates = this.extractCoordinates(feature.geometry);
      const polyline = L.polyline(coordinates, { color: 'blue' }).addTo(this.map);
      polyline.bindPopup(`Name: ${feature.properties.name}<br>Description: ${feature.properties.description}`);
    });
  }

  private extractCoordinates(geometry: string): L.LatLng[] {
    const regex = /LINESTRING \((.*?)\)/;
    const match = regex.exec(geometry);
    if (match && match[1]) {
      const coords = match[1]
        .split(',')
        .map(coord => {
          const [lng, lat] = coord.trim().split(' ').map(Number);
          return L.latLng(lat, lng); // Leaflet uses [lat, lng]
        });
      return coords;
    }
    return [];
  }
}
