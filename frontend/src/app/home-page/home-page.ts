import { Component, inject } from '@angular/core';
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

  date = new Date().toLocaleDateString('en-CA', { timeZone: 'Canada/Eastern' }).replace(/\//g, '-');
  scoresResource = httpResource<GameDetails[]>(() => `${this.globalConfig.backendURL}/scores/${this.date}`)
}
