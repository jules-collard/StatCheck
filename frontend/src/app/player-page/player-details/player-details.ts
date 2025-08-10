import { Component, DestroyRef, inject, input, signal, OnInit } from '@angular/core';
import { PlayerService } from '../player.service';
import { Player } from '../player.model';
import { AgePipe } from '../../pipes/age.pipe';
import { HeightPipe } from '../../pipes/height.pipe';
import { PositionPipe } from '../../pipes/position.pipe';

@Component({
  selector: 'app-player-details',
  imports: [AgePipe, HeightPipe, PositionPipe],
  templateUrl: './player-details.html',
  styleUrl: './player-details.css'
})
export class PlayerDetails {
  playerData = input.required<Player>()
}
