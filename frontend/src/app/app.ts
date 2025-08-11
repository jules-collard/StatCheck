import { Component, signal } from '@angular/core';
import { Search } from "./search/search";
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [Search, RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('StatCheck');
}
