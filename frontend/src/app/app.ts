import { Component, DestroyRef, inject, OnInit, signal } from '@angular/core';
import { PlayerPage } from "./player-page/player-page";

@Component({
  selector: 'app-root',
  imports: [PlayerPage],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('StatCheck');
  
}
