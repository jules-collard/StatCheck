import { Component, computed, DestroyRef, inject, input, OnInit, signal } from '@angular/core';

import { PlayerDetails } from "./player-details/player-details";
import { PlayerService } from './player.service';
import { ActivatedRoute, ActivatedRouteSnapshot, ResolveFn, RouterStateSnapshot } from '@angular/router';
import { SkaterStats } from './skater-stats.model';
import { Player } from './player.model';
import { Award } from './award.model';
import { SkaterTotalsTable } from './skater-totals-table/skater-totals-table';
import { GoalieTotalsTable } from "./goalie-totals-table/goalie-totals-table";
import { GoalieStats } from './goalie-stats.model';
import { SkaterAnalyticsTable } from './skater-analytics-table/skater-analytics-table';
import { GoalieAdvancedTable } from './goalie-advanced-table/goalie-advanced-table';
import { SkaterOnIceTable } from "./skater-onice-table/skater-onice-table";
import { httpResource, HttpResourceRef } from '@angular/common/http';

@Component({
  selector: 'app-player-page',
  imports: [PlayerDetails, SkaterTotalsTable, GoalieTotalsTable, SkaterAnalyticsTable, GoalieAdvancedTable, SkaterOnIceTable],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css'
})
export class PlayerPage {
  regularSeason = signal<boolean>(true)

  playerInfoResource = input.required<HttpResourceRef<Player | undefined>>()
  regSeasonResource = input.required<HttpResourceRef<SkaterStats[] | GoalieStats[] | undefined>>()
  postSeasonResource = input.required<HttpResourceRef<SkaterStats[] | GoalieStats[] | undefined>>()

  private awardNames = ['Vezina Trophy', 'Hart Memorial Trophy', 'Calder Memorial Trophy', 'James Norris Memorial Trophy', 'Frank J. Selke Trophy', 'Conn Smythe Trophy', 'Stanley Cup']

  playerData = computed<Player | null>(() => {
    if (this.playerInfoResource().hasValue()) {
      return this.playerInfoResource().value()!
    } else {
      return null
    }
  })

  regSeasonStats = computed<SkaterStats[] | GoalieStats[] | null>(() => {
    if (this.regSeasonResource().hasValue()) {
      return this.regSeasonResource().value()!
    } else {
      return null
    }
  })

  postSeasonStats = computed<SkaterStats[] | GoalieStats[] | null>(() => {
    if (this.postSeasonResource().hasValue()) {
      return this.postSeasonResource().value()!
    } else {
      return null
    }
  })

  stats = computed<SkaterStats[] | GoalieStats[] | null>(() => {
    return this.regularSeason() ? this.regSeasonStats() : this.postSeasonStats()
  })

  awards = computed<Award[]>(() => {
    return this.playerData()?.awards.filter((award) => {
      return this.awardNames.includes(award.awardName)
    }) ?? [];
  })

  selectPlayoffs() {
    this.regularSeason.set(false)
  }

  selectRegular() {
    this.regularSeason.set(true)
  }

}

const PLAYER_URL = 'http://localhost:5000/api/players'

export const resolvePlayer: ResolveFn<HttpResourceRef<Player | undefined>> = (activatedRoute: ActivatedRouteSnapshot, routerState: RouterStateSnapshot) => {
  const playerID = Number(activatedRoute.paramMap.get('playerID'))
  return httpResource<Player>(() => `${PLAYER_URL}/${playerID}`)
};

export const resolveRegSeasonStats: ResolveFn<HttpResourceRef<SkaterStats[] | GoalieStats[] | undefined>> = (activatedRoute: ActivatedRouteSnapshot, routerState: RouterStateSnapshot) => {
  const playerID = Number(activatedRoute.paramMap.get('playerID'))
  return httpResource<SkaterStats[] | GoalieStats[]>(() => `${PLAYER_URL}/${playerID}/stats?gameType=2`)
};

export const resolvePostSeasonStats: ResolveFn<HttpResourceRef<SkaterStats[] | GoalieStats[] | undefined>> = (activatedRoute: ActivatedRouteSnapshot, routerState: RouterStateSnapshot) => {
  const playerID = Number(activatedRoute.paramMap.get('playerID'))
  return httpResource<SkaterStats[] | GoalieStats[]>(() => `${PLAYER_URL}/${playerID}/stats?gameType=3`)
};
