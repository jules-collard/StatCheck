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
      case 'FUT': return [this.gameDetails().homeTeam.abbrev, this.gameDetails().awayTeam.abbrev]
      default: return [this.gameDetails().homeTeam.score, this.gameDetails().awayTeam.score]
    }
  })

  scoreDetails = computed(() => {
    switch (this.gameDetails().gameState) {
      case 'FUT': return [this.gameDetails().homeTeam.record, this.gameDetails().awayTeam.record]
      default: return [`SOG: ${this.gameDetails().homeTeam.sog}`, `SOG: ${this.gameDetails().awayTeam.sog}`]
    }
  })

  timeShow = computed(() => {
    switch (this.gameDetails().gameState) {
      case 'LIVE': case 'CRIT': return this.gameDetails().clock?.timeRemaining;
      case 'OVER': case 'FINAL': case 'OFF': return this.gameDetails().gameOutcome?.lastPeriodType === 'REG' ? 'FINAL' : `FINAL (${this.gameDetails().gameOutcome?.lastPeriodType})`
      default: return `${this.gameDetails().startTimeEastern} ET`;
    }
  })

}
