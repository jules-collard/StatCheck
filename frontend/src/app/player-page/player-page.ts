import { Component } from '@angular/core';

import { PlayerDetails } from "./player-details/player-details";
import { PlayerSeasonTotals } from "./player-season-totals/player-season-totals";

@Component({
  selector: 'app-player-page',
  imports: [PlayerDetails, PlayerSeasonTotals],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css'
})
export class PlayerPage {

}
