import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerInfo } from './player-info';

describe('PlayerInfo', () => {
  let component: PlayerInfo;
  let fixture: ComponentFixture<PlayerInfo>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayerInfo]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlayerInfo);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
