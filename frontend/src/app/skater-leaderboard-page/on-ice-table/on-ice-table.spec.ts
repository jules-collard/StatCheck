import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OnIceTable } from './on-ice-table';

describe('OnIceTable', () => {
  let component: OnIceTable;
  let fixture: ComponentFixture<OnIceTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OnIceTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OnIceTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
