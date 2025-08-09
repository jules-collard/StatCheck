import { Component, DestroyRef, inject, input, signal, OnInit } from '@angular/core';
import { PlayerSeasonTotalsService } from './player-season-totals.service';
import { SeasonTotals } from './season-totals.model';
import { SeasonPipe } from '../../pipes/season.pipe';

@Component({
  selector: 'app-player-season-totals',
  imports: [SeasonPipe],
  templateUrl: './player-season-totals.html',
  styleUrl: './player-season-totals.css'
})
export class PlayerSeasonTotals implements OnInit {
  private destroyRef = inject(DestroyRef);
  private seasonTotalService = inject(PlayerSeasonTotalsService)

  id = input.required<number>();
  seasons = signal<SeasonTotals[]>([])
  error = signal('')

  ngOnInit() {
    const subscription = this.seasonTotalService.fetchSeasonTotals(this.id()).subscribe({
      next: (resData) => {
        this.seasons.set(resData);
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

}
