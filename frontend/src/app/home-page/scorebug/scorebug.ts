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

  scoreShow = computed(() => {
    switch (this.gameDetails().gameState) {
      case 'FUT': case 'PRE': return [0, 0]
      default: return [this.gameDetails().homeTeam.score, this.gameDetails().awayTeam.score]
    }
  })

  scoreDetails = computed(() => {
    switch (this.gameDetails().gameState) {
      case 'FUT': return [this.gameDetails().homeTeam.record, this.gameDetails().awayTeam.record]
      default: return [`SOG: ${this.gameDetails().homeTeam.sog}`, `SOG: ${this.gameDetails().awayTeam.sog}`]
    }
  })

}
