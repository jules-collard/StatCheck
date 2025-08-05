import { Component, input } from '@angular/core';

import { PlayerInfo } from './player-info/player-info';
import { PlayerStats } from './player-stats/player-stats';

@Component({
  selector: 'app-player-page',
  imports: [PlayerInfo, PlayerStats],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css'
})
export class PlayerPage {;
  id = input.required<number>()
}
