import { Component, computed, input } from '@angular/core';
import { TeamScore } from './team-score.model';
import { GameState } from './game-state.model';

@Component({
  selector: 'app-scorebug',
  imports: [],
  templateUrl: './scorebug.html',
  styleUrl: './scorebug.css'
})
export class Scorebug {
  home = input.required<TeamScore>();
  away = input.required<TeamScore>();
  state = input.required<GameState>();

  stateShow = computed<string>(() => {
    if (this.state().finished) {
      return `Final (${this.state().lastPeriodType})`
    } else {
      return this.state().timeRemaining;
    }
  })
}
