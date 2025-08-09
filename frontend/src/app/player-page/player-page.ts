import { Component, input } from '@angular/core';

import { PlayerDetails } from "./player-details/player-details";

@Component({
  selector: 'app-player-page',
  imports: [PlayerDetails],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css'
})
export class PlayerPage {;
  id = input.required<number>()
}
