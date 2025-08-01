import { Component, computed, input } from '@angular/core';
import { Player } from '../player.model';
import { MatCardModule } from '@angular/material/card';
import { AgePipe } from '../../pipes/age.pipe';
import { HeightPipe } from '../../pipes/height-pipe';

@Component({
  selector: 'app-player-info',
  imports: [MatCardModule, AgePipe, HeightPipe],
  templateUrl: './player-info.html',
  styleUrl: './player-info.css'
})
export class PlayerInfo {
  playerData = input.required<Player>()
}
