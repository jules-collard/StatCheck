import { Component, computed, inject, signal } from '@angular/core';
import { Scorebug } from "./scorebug/scorebug";
import { httpResource } from '@angular/common/http';
import { GlobalConfigService } from '../shared/global-config.service';
import { GameDetails } from './game-details.model';

@Component({
  selector: 'app-home-page',
  imports: [Scorebug],
  templateUrl: './home-page.html',
  styleUrl: './home-page.css'
})
export class HomePage {
  globalConfig = inject(GlobalConfigService)

  date = signal(new Date())
  dateString = computed(() => this.date().toLocaleDateString('en-CA', {
    timeZone: 'Canada/Eastern',
    weekday: 'long',
    month: 'long',
    day: 'numeric'
  }))

  dateForQuery = computed(() => this.date().toLocaleDateString('en-CA', { timeZone: 'Canada/Eastern' }).replace(/\//g, '-'))
  scoresResource = httpResource<GameDetails[]>(() => `${this.globalConfig.backendURL}/scores/${this.dateForQuery()}`)

  addDays(date: Date, days: number) {
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }

  moveDay(diff: number) {
    this.date.set(this.addDays(this.date(), diff))
  }
}
