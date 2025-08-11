import { Component, DestroyRef, inject, OnInit, signal } from '@angular/core';
import { PlayerPage } from "./player-page/player-page";
import { Search } from "./search/search";

@Component({
  selector: 'app-root',
  imports: [PlayerPage, Search],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('StatCheck');
  playerID = signal<number>(8481461)
}
