import { Component, input } from '@angular/core';
import { AgePipe } from '../../pipes/age.pipe';
import { HeightPipe } from '../../pipes/height.pipe';
import { PositionPipe } from '../../pipes/position.pipe';
import { Player } from '../player.model';

@Component({
  selector: 'app-player-details',
  imports: [AgePipe, HeightPipe, PositionPipe],
  templateUrl: './player-details.html',
  styleUrl: './player-details.css'
})
export class PlayerDetails {  
  playerData = input.required<Player>()
}
