import { Component, DestroyRef, inject, input, OnInit, signal } from '@angular/core';
import { PlayerStatsService } from './player-stats.service';
import { SeasonStats } from './season-stats.model';
import { MatTableModule } from '@angular/material/table';
import { ColNamePipe } from '../../pipes/colname.pipe';

@Component({
  selector: 'app-player-stats',
  imports: [MatTableModule, ColNamePipe],
  templateUrl: './player-stats.html',
  styleUrl: './player-stats.css'
})
export class PlayerStats implements OnInit {
  private destroyRef = inject(DestroyRef);
  private playerStatsService = inject(PlayerStatsService)
  
  id = input.required<number>()
  stats = signal<SeasonStats[]>([])
  error = signal('')

  columnsToDisplay = [
    'season', 'goals', 'primaryAssists', 'secondaryAssists', 'hits', 'sog', 'blocks', 'penaltyMinutes', 'takeaways', 'giveaways'
  ]

  ngOnInit() {
    const subscription = this.playerStatsService.fetchPlayerStats(this.id()).subscribe({
      next: (resData) => {
        this.stats.set(resData)
        console.log(this.stats())
      },
      error: (error) => {
        console.log(error)
        this.error.set("Error fetching player stats.")
      }
    });

    this.destroyRef.onDestroy(() => {
      subscription.unsubscribe();
    });
  }
}
