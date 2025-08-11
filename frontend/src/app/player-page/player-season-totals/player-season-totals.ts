import { Component, inject, computed } from '@angular/core';
import { SeasonPipe } from '../../pipes/season.pipe';
import { Award } from '../award.model';
import { AwardBadge } from './award-badge/award-badge';
import { PlayerService } from '../player.service';
import { Player } from '../player.model';
import { SeasonTotals } from './season-totals.model';

@Component({
  selector: 'app-player-season-totals',
  imports: [SeasonPipe, AwardBadge],
  templateUrl: './player-season-totals.html',
  styleUrl: './player-season-totals.css'
})
export class PlayerSeasonTotals {
  private playerService = inject(PlayerService)
  
  playerData = computed<Player | null>(() => {
    return this.playerService.getPlayerData()
  })
  seasonTotals = computed<SeasonTotals[] | null>(() => {
    return this.playerService.getSeasonTotals()
  })
  awards = computed<Award[]>(() => {
    return this.playerData()?.awards ?? []
  })
  loading = computed<boolean>(() => {
    return this.playerService.playerDataIsLoading() || this.playerService.seasonTotalsIsLoading()
  })

  private awardsToDisplay = ['Stanley Cup', 'Conn Smythe Trophy', 'Vezina Trophy', 'Hart Memorial Trophy', 'Calder Memorial Trophy', 'James Norris Memorial Trophy', 'Frank J. Selke Trophy']
  
  getSeasonAwards(season: number) {
    var seasonAwards: string[] = [];
    for (const award of this.awards()) {
        if (award.season == season && this.awardsToDisplay.includes(award.awardName)) {
          seasonAwards.push(award.awardName)
        } 
    }
    return seasonAwards
  }

}
