import { Component, DestroyRef, inject, input, signal, OnInit } from '@angular/core';
import { SeasonTotals } from './season-totals.model';
import { SeasonPipe } from '../../pipes/season.pipe';
import { Award } from '../award.model';
import { AwardBadge } from './award-badge/award-badge';
import { PlayerService } from '../player.service';

@Component({
  selector: 'app-player-season-totals',
  imports: [SeasonPipe, AwardBadge],
  templateUrl: './player-season-totals.html',
  styleUrl: './player-season-totals.css'
})
export class PlayerSeasonTotals implements OnInit {
  private destroyRef = inject(DestroyRef);
  private playerService = inject(PlayerService)

  id = input.required<number>();
  awards = input<Award[]>([])
  seasons = signal<SeasonTotals[]>([])
  error = signal('')
  isFetching = signal(false)

  private awardsToDisplay = ['Stanley Cup', 'Conn Smythe Trophy', 'Vezina Trophy', 'Hart Memorial Trophy', 'Calder Memorial Trophy', 'James Norris Memorial Trophy', 'Frank J. Selke Trophy']

  ngOnInit() {
    this.isFetching.set(true)
    const subscription = this.playerService.fetchSeasonTotals(this.id()).subscribe({
      next: (resData) => {
        this.seasons.set(resData);
      },
      complete: () => {
        this.isFetching.set(false)
      },
      error: (error) => {
        console.log(error)
        this.error.set("Error fetching player season totals.")
      }
    });

    this.destroyRef.onDestroy(() => {
      subscription.unsubscribe();
    });
  }

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
