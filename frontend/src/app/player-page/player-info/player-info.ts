import { Component, input } from '@angular/core';
import { Player } from '../player.model';
import { MatCardModule } from '@angular/material/card';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-player-info',
  imports: [MatCardModule, DatePipe],
  templateUrl: './player-info.html',
  styleUrl: './player-info.css'
})
export class PlayerInfo {
  playerData = input.required<Player>()
}
