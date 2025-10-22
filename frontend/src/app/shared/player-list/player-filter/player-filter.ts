import { Component, computed, effect, inject, input, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Control, form } from '@angular/forms/signals';
import { PlayerListService } from '../player-list.service';
import { FilterParams } from './filter-params.interface';

@Component({
  selector: 'app-player-filter',
  imports: [FormsModule, Control],
  templateUrl: './player-filter.html',
  styleUrl: './player-filter.css'
})
export class PlayerFilter {
  playerListService = inject(PlayerListService);
  
  positionOptions = input<{goalie: boolean, defenseman: boolean, forward: boolean}>({
    goalie: true,
    defenseman: true,
    forward: true
  })
  anyPositions = computed<boolean>(() => {
    return this.positionOptions().goalie || this.positionOptions().defenseman || this.positionOptions().forward;
  })

  team = 'All';
  nameToSearch = signal<string>('');

  searchEffect = effect(() => {
    this.playerListService.filterParams.update(params =>
      ({...params, nameToSearch: this.nameToSearch()})
    )
  })

  activeRetired = signal<{active: boolean; retired: boolean;}>({
    active: false,
    retired: false
  })

  activeRetiredForm = form(this.activeRetired);

  onChangeActiveRetired() {
    if (!(this.activeRetiredForm.active().value() || this.activeRetiredForm.retired().value())) {
      this.playerListService.filterParams.update(params =>
        ({...params, active: true, retired: true})
      );
    } else {
      this.playerListService.filterParams.update(params =>
        ({...params, active: this.activeRetiredForm.active().value(), retired: this.activeRetiredForm.retired().value()})
      );
    }
  }

  resetActiveRetired() {
    this.activeRetiredForm.active().value.set(false)
    this.activeRetiredForm.retired().value.set(false)
    this.onChangeActiveRetired()
  }

  position = signal<{goalie: boolean, defenseman: boolean, forward: boolean}>({
    goalie: false,
    defenseman: false,
    forward: false
  });

  positionForm = form(this.position);

  onChangePosition() {
    if (!(this.positionForm.goalie().value() || this.positionForm.defenseman().value() || this.positionForm.forward().value())) {
      this.playerListService.filterParams.update(params =>
        ({...params, goalie: true, defenseman: true, forward: true})
      )
    } else {
      this.playerListService.filterParams.update(params =>
        ({...params, goalie: this.positionForm.goalie().value(), defenseman: this.positionForm.defenseman().value(), forward: this.positionForm.forward().value()})
      )
    }
  }

  resetPosition() {
    this.positionForm.goalie().value.set(false)
    this.positionForm.defenseman().value.set(false)
    this.positionForm.forward().value.set(false)
    this.onChangePosition()
  }

  onTeamChange() {
    this.playerListService.filterParams.update(params => ({...params, team: this.team}))
  }
}
