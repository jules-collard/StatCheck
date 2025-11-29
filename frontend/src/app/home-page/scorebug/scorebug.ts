import { Component, computed, input } from '@angular/core';
import { GameDetails } from '../game-details.model';

@Component({
  selector: 'app-scorebug',
  imports: [],
  templateUrl: './scorebug.html',
  styleUrl: './scorebug.css'
})
export class Scorebug {
  gameDetails = input.required<GameDetails>();
}
