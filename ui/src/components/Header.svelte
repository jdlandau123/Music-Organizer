<script>
    import TopAppBar, { Row, Section, Title } from '@smui/top-app-bar';
    import { recordsOnDevice } from '../stores/collectionStore';
</script>

<TopAppBar class="appbar" color={'primary'} variant="standard">
    <Row>
      <Section>
        <Title class="title">Music Organizer</Title>
      </Section>
      <Section align={'end'} style="margin-right: 20px; font-size: 14pt;">
        {$recordsOnDevice.length} records synced
      </Section>
    </Row>
</TopAppBar>

<style>
    /* Hide everything above this component. */
    :global(#smui-app),
    :global(body),
    :global(html) {
      display: block !important;
      height: auto !important;
      width: auto !important;
      position: static !important;
    }

    :global(.appbar) {
        /* background-color: green; */
        color: white;
        font-size: 18pt;
        height: 65px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }

    :global(.title) {
        padding: 20px;
    }
</style>